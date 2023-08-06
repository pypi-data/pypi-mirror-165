"""Server implementation."""

# Copyright 2022 LW016 (GPG FINGERPRINT 33CA C1E8 EC4C 0B31 73AE  DD8B 31A5 35D1 2844 39ED)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ssl

from time import time
from logging import Logger, getLogger
from typing import Callable, Optional, Union, Dict, Set

from uuid import uuid4
from base64 import b64encode, b64decode
from binascii import Error as BinError

from asyncio import (sleep, create_task, start_server,
        LimitOverrunError, IncompleteReadError, CancelledError)

from asyncio.streams import StreamReader, StreamWriter
from asyncio.events import AbstractServer
from asyncio.tasks import Task


try:
    import ujson as json

except ImportError:
    import json # type: ignore

try:
    from uvloop import install as tune

except ImportError:
    pass


class SaydServer:
    """Server class.

    :param host: A list of addresses or a address to bind the server, defaults to `None`.
    :type host: Optional[Union[str, list]]
    :param port: Port to use, defaults to `7050`.
    :type port: int
    :param queue: Limit of clients waiting to connect, defaults to `512`.
    :type queue: int
    :param limit: Limit of connected clients, defaults to `1024`.
    :type limit: int
    :param buffer: Buffer size limit per client in KiB, defaults to `128`.
    :type buffer: int
    :param timeout: Time in seconds to disconnect a client that is not responding,\
            defaults to `3`.
    :type timeout: int
    :param ping: Frequency in seconds to ping the clients, defaults to `1`.
    :type ping: int
    :param logger: Logger to use, defaults to `None`.
    :type logger: Optional[Logger]
    :param cert: Path to the TLS certificate, defaults to `None`.
    :type cert: Optional[str]
    :param cert_key: Path to the TLS certificate key, defaults to `None`.
    :type cert_key: Optional[str]
    """

    def __init__(
            self,
            host: Optional[Union[str, list]] = None,
            port: int = 7050,
            queue: int = 512,
            limit: int = 1024,
            buffer: int = 128,
            timeout: int = 3,
            ping: int = 1,
            logger: Optional[Logger] = None,
            cert: Optional[str] = None,
            cert_key: Optional[str] = None
            ) -> None:

        self._host = host
        self._port = port

        self._queue_limit = queue
        self._connections_limit = limit
        self._buffer_limit = buffer * 1024
        self._connection_timeout = timeout
        self._ping_timeout = ping


        if logger is not None:
            self._logger = logger

        else:
            self._logger = getLogger()


        self._ssl_context: Union[ssl.SSLContext, bool, None]

        if cert is not None and cert_key is not None:
            self._ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self._ssl_context.load_cert_chain(cert, cert_key)

        else:
            self._ssl_context = None
        

        self._server: AbstractServer
        self._ping_task: Task
        
        self._connections: Dict[tuple, list] = {}
        self._connections_queue: Dict[tuple, list] = {}
        self._blacklist: Set[str] = set()

        self._callbacks: Dict[str, Callable] = {
                "ping": self._ping
                }

        self._call_tasks: Set[Task] = set()
        self._calls: Dict[str, Union[dict, list, None]] = {}

        
        try:
            # Enable uvloop if available.
            tune()

        except NameError:
            pass


    @property
    def clients(self) -> Set[tuple]:
        """Returns the connected clients.

        :return: A set containing the clients.
        :rtype: Set[tuple]
        """

        return set(self._connections.keys())

    
    def callback(self, name: str) -> Callable:
        """Decorator to bind functions to be called when a request is received.

        :param name: Name to bind the function.
        :type name: str
        """

        assert name != "ping", "Name 'ping' is used internally."

        def decorator(function: Callable) -> Callable:
            self._callbacks.update({name: function})

            def wrapper(address: tuple, instance: Union[str, None], data: dict) -> Callable: # pylint: disable=unused-argument
                return function(address, instance, data)

            return wrapper

        return decorator

    
    def add_callback(self, name: str, function: Callable) -> None:
        """Method to bind functions to be called when a request is received.

        :param name: Name to bind the function.
        :type name: str
        :param function: Function to bind.
        :type function: Callable
        """

        assert name != "ping", "Name 'ping' is used internally."

        self._callbacks.update({name: function})


    def blacklist(self, host: str) -> None:
        """Method to add a host to the blacklist.

        :param host: Host to block.
        :type host: str
        """

        self._blacklist.add(host)
        self._logger.info("Server | Host %s added to the blacklist", host)
        
        # Closes connections from the blacklisted host.
        for connection in list(self._connections.keys()):
            if connection[0] == host:
                if not self._connections[connection][0].is_closing():
                    self._connections[connection][0].close()


    def unblacklist(self, host: str) -> None:
        """Method to remove a host from the blacklist.

        :param host: Host to unblock.
        :type host: str
        """

        self._blacklist.discard(host)
        self._logger.info("Server | Host %s removed from the blacklist", host)


    async def call(
            self,
            name: str,
            data: Optional[dict] = None,
            instance: Optional[str] = None,
            address: Optional[tuple] = None,
            wait: bool = True,
            wait_timeout: int = 3,
            _call_id: Optional[str] = None
            ) -> Union[dict, list, bool, Exception, None]:
        """Calls a function in a remote client or in all clients (broadcast) if address
        is not specified.

        :param name: Name of the function.
        :type name: str
        :param data: Data to send, defaults to `None`.
        :type data: dict
        :param instance: Instance to pass to the remote function, defaults to `None`.
        :type instance: Optional[str]
        :param address: Client address, defaults to `None`.
        :type address: Optional[tuple]
        :param wait: `True` to wait for a answer, defaults to `True`.
        :type wait: bool
        :param wait_timeout: Time limit in seconds to wait for a answer, defaults to `3`.
        :type wait_timeout: int
        :return: The call result.
        :rtype: Union[dict, list, bool, Exception, None]
        """
        
        if data is not None:
            assert "call" not in data, "Key 'call' is used internally."
            assert "call_id" not in data, "Key 'call_id' is used internally."
            assert "instance" not in data, "Key 'instance' is used internally."
        
        
        datap: dict = data.copy() if data is not None else {}
        datap.update({
            "call": name,
            "instance": instance
            })

        
        to_wait: bool = False

        if _call_id is not None:
            datap.update({"call_id": _call_id})

        elif wait:
            to_wait = True

            call_id: str = uuid4().hex
            self._calls.update({call_id: [] if address is None else None})

            datap.update({"call_id": call_id})

        
        try:
            dataf: bytes = b64encode(json.dumps(datap).encode("ascii")) + b"&"

            if address is not None:
                if not self._connections[address][0].is_closing():
                    self._connections[address][0].write(dataf)
                    await self._connections[address][0].drain()
                
            else:
                for connection in list(self._connections.keys()):
                    if not self._connections[connection][0].is_closing():
                        self._connections[connection][0].write(dataf)
                        await self._connections[connection][0].drain()

        except (SyntaxError, RuntimeError, KeyError, TypeError,
                ValueError, AssertionError, ConnectionError) as error:

            return error
        
        
        if to_wait:
            start_t: float = time()
            
            # Wait for a answer.
            if address is None:
                con_max: int = len(self._connections)

                while len(self._calls[call_id]) < con_max and (time() - start_t) < wait_timeout: # type: ignore
                    await sleep(0.01)

            else:
                while self._calls[call_id] is None and (time() - start_t) < wait_timeout:
                    await sleep(0.01)

            # If was not answered returns None.
            if self._calls[call_id] is None or (isinstance(self._calls[call_id], list) and len(self._calls[call_id]) == 0): # type: ignore
                del self._calls[call_id]
                return None
            
            # If was answered returns the response.
            answer: Union[dict, list] = self._calls[call_id] # type: ignore
            del self._calls[call_id]
            return answer
        
        return True

    
    async def start(self) -> None:
        """Starts the server."""

        if self._ssl_context is not None:
            ssl_data = {
                    "ssl": self._ssl_context,
                    "ssl_handshake_timeout": self._connection_timeout*2
                    }

        else:
            ssl_data = {}
        
        
        self._server = await start_server(
                self._connection_bootstrap,
                host=self._host, # type: ignore
                port=self._port,
                limit=self._buffer_limit,
                backlog=self._queue_limit,
                start_serving=True,
                **ssl_data) # type: ignore

        self._ping_task = create_task(self._ping_clients())


    async def stop(self) -> None:
        """Stops the server."""

        self._ping_task.cancel()

        # Closes queued connections.
        for connection in list(self._connections_queue.keys()):
            if not self._connections_queue[connection][0].is_closing():
                self._connections_queue[connection][0].close()
            
            self._connections_queue[connection][2].cancel()
            del self._connections_queue[connection]

        # Closes open connections.
        for connection in list(self._connections.keys()):
            if not self._connections[connection][0].is_closing():
                self._connections[connection][0].close()
            
            self._connections[connection][2].cancel()
            del self._connections[connection]

        self._server.close()

    
    async def _ping_clients(self) -> None:
        """Continuously check the connection status of the clients."""

        while 1:
            current_time = time()

            # Checks queued connections.
            for connection in list(self._connections_queue.keys()):
                # Checks if the connection is closed.
                if self._connections_queue[connection][0].is_closing():
                    self._connections_queue[connection][2].cancel()
                    del self._connections_queue[connection]

                # Checks if the client stopped responding.
                elif (current_time - self._connections_queue[connection][1]) >= self._connection_timeout: 
                    if not self._connections_queue[connection][0].is_closing():
                        self._connections_queue[connection][0].close()

                    self._connections_queue[connection][2].cancel()
                    del self._connections_queue[connection]

            # Checks open connections.
            for connection in list(self._connections.keys()):
                # Checks if the connection is closed.
                if self._connections[connection][0].is_closing():
                    self._connections[connection][2].cancel()
                    del self._connections[connection]

                    self._logger.info("Server | Disconnection from %s:%s", connection[0], connection[1])
                
                # Checks if the client stopped responding.
                elif (current_time - self._connections[connection][1]) >= self._connection_timeout: 
                    if not self._connections[connection][0].is_closing():
                        self._connections[connection][0].close()

                    self._connections[connection][2].cancel()
                    del self._connections[connection]

                    self._logger.info("Server | Disconnection from %s:%s", connection[0], connection[1])
                
                # Ping the client.
                else:
                    await self.call(name="ping", address=connection, wait=False)

            await sleep(self._ping_timeout)

    
    async def _ping(self, address: tuple, instance: None, data: dict) -> None: # pylint: disable=unused-argument
        """Called when a ping is received from a client."""

        try:
            self._connections[address][1] = time()

        except KeyError as error:
            self._logger.error("Server | Ping receive error (%s)", error)


    async def _connection_bootstrap(self, reader: StreamReader, writer: StreamWriter) -> None:
        address: tuple = writer.get_extra_info("peername")

        
        if address is None or address[0] in self._blacklist or address in self._connections_queue\
                or address in self._connections:

            writer.close()

        elif (len(self._connections)+len(self._connections_queue))+1 > self._connections_limit:
            writer.close()

            self._logger.info("Server | Connection rejected from %s:%s (max capacity)", address[0], address[1])

        else:
            task: Task = create_task(self._connection_handler(reader, address))

            self._connections_queue.update({address: [writer, time(), task]})
 

    async def _connection_handler(self, reader: StreamReader, address: tuple) -> None:
        stream_reader = reader

        recv_data: Union[bytes, str]
        raw_data: str
        data: dict
        
        call: str
        call_id: Union[str, None]
        instance: str
        task: Task

        queued: bool = True
        header: Union[str, list]
        header_addr: tuple


        async def reset_buffer(timeout: float = 0) -> None:
            try:
                del recv_data, raw_data, data, call, call_id, instance, task

            except NameError:
                pass

            await sleep(timeout)


        while 1:
            try:
                try:
                    recv_data = await stream_reader.readuntil(b"&")

                except LimitOverrunError:
                    self._logger.info("Server | Buffer limit exceeded for host %s:%s", address[0], address[1])

                    await reset_buffer(0.1)
                    continue

                except (IncompleteReadError, ConnectionError):
                    await reset_buffer(0.1)
                    continue


                if queued:
                    raw_data = recv_data.decode("ascii")

                    # Checks if the data has a proxy protocol header.
                    if raw_data.find("PROXY") != -1:
                        header, recv_data = raw_data.split("\n")
                        recv_data = recv_data.encode("ascii")

                        header = header.split(" ")
                        header_addr = (header[2], int(header[4]))
                        
                        # Verify if the address is valid.
                        if header_addr[0] in self._blacklist or header_addr in self._connections:
                            self._connections_queue[address][0].close()
                            return
                        
                        self._connections.update({header_addr: self._connections_queue[address]})
                        del self._connections_queue[address]

                        address = header_addr
                    
                    elif raw_data.find("UNKNOWN") != -1:
                        self._connections_queue[address][0].close()
                        return

                    else:
                        self._connections.update({address: self._connections_queue[address]})
                        del self._connections_queue[address]
                    
                    self._logger.info("Server | Connection from %s:%s", address[0], address[1])
                    queued = False


                raw_data = b64decode(recv_data[:-1].decode("ascii")) # type: ignore
                data = json.loads(raw_data)


                if "call_id" in data:
                    call_id = data.pop("call_id")
                    
                    # Checks if the data is a answer of a previous call.
                    if call_id in self._calls:
                        del data["call"]
                        del data["instance"]
                        
                        data.update({"address": address})

                        if isinstance(self._calls[call_id], list):
                            self._calls[call_id].append(data) # type: ignore

                        else:
                            self._calls[call_id] = data

                        await reset_buffer()
                        continue

                else:
                    call_id = None


                call = data.pop("call")
                instance = data.pop("instance")


                if call in self._callbacks:
                    task = create_task(self._callbacks[call](address, instance, data))

                    setattr(task, "call_id", call_id)
                    setattr(task, "call_name", call)
                    setattr(task, "call_instance", instance)
                    setattr(task, "call_address", address)

                    self._call_tasks.add(task)
                    task.add_done_callback(self._on_call_exit)

                elif "*" in self._callbacks:
                    task = create_task(self._callbacks["*"](address, instance, data))
                    
                    setattr(task, "call_id", call_id)
                    setattr(task, "call_name", call)
                    setattr(task, "call_instance", instance)
                    setattr(task, "call_address", address)

                    self._call_tasks.add(task)
                    task.add_done_callback(self._on_call_exit)

            
            except (json.JSONDecodeError, BinError, KeyError, TypeError,
                    ValueError, IndexError, UnicodeDecodeError) as error:
                
                self._logger.error("Server | Error in the data received (%s)", error)

                await reset_buffer(0.1)
                continue

            await reset_buffer()


    def _on_call_exit(self, task: Task) -> None:
        result: Union[None, dict]

        try:
            result = task.result()

        except CancelledError:
            result = None

        if result is not None and isinstance(result, dict) and task.call_id is not None: # type: ignore
            try:
                rtask: Task = create_task(self.call(
                    name=task.call_name, # type: ignore
                    data=result,
                    instance=task.call_instance, # type: ignore
                    address=task.call_address, # type: ignore
                    wait=False,
                    _call_id=task.call_id # type: ignore
                    ))

                self._call_tasks.add(rtask)
                rtask.add_done_callback(self._call_tasks.discard)

            except AssertionError:
                pass

        self._call_tasks.discard(task)
