"""Client implementation."""

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

from asyncio import (sleep, create_task, open_connection,
        LimitOverrunError, IncompleteReadError, CancelledError)

from asyncio.streams import StreamReader, StreamWriter
from asyncio.tasks import Task


try:
    import ujson as json

except ImportError:
    import json # type: ignore

try:
    from uvloop import install as tune

except ImportError:
    pass


class SaydClient:
    """Client class.
    
    :param host: Server hostname, defaults to localhost.
    :type host: str
    :param port: Server port, defaults to `7050`.
    :type port: int
    :param local_host: Local address to bind the client, defaults to `None`.
    :type local_host: str
    :param local_port: Local port to bind the client, defaults to `None`.
    :type local_port: Optional[Union[int, str]]
    :param buffer: Buffer size limit in KiB, defaults to `128`.
    :type buffer: int
    :param timeout: Time in seconds to disconnect from the server if is not responding,\
            defaults to `3`.
    :type timeout: int
    :param ping: Frequency in seconds to ping the server, defaults to `1`.
    :type ping: int
    :param reconnect: If disconnected from the server try to reconnect, defaults to `True`.
    :type reconnect: bool
    :param reconnect_timeout: Frequency in seconds to try to reconnect if disconnected,\
            defaults to `5`.
    :type reconnect_timeout: int
    :param logger: Logger to use, defaults to `None`.
    :type logger: Optional[Logger]
    :param cert: Path to the TLS certificate, defaults to `None`.
    :type cert: Optional[str]
    """

    def __init__(
            self,
            host: str = "localhost",
            port: int = 7050,
            local_host: Optional[str] = None,
            local_port: Optional[Union[int, str]] = None,
            buffer: int = 128,
            timeout: int = 3,
            ping: int = 1,
            reconnect: bool = True,
            reconnect_timeout: int = 5,
            logger: Optional[Logger] = None,
            cert: Optional[str] = None
            ) -> None:

        self._host = host
        self._port = port
        self._dlocal_host = local_host
        self._dlocal_port = local_port
        
        self._buffer_limit = buffer * 1024
        self._connection_timeout = timeout
        self._ping_timeout = ping

        self._reconnect = reconnect
        self._reconnect_timeout = reconnect_timeout


        if logger is not None:
            self._logger = logger

        else:
            self._logger = getLogger()

        
        self._ssl_context: Union[ssl.SSLContext, bool, None]

        if cert is not None:
            self._ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cert)

        else:
            self._ssl_context = None

        
        self._writer: StreamWriter
        self._reader: StreamReader
        self._client_task: Task
        self._ping_task: Task
        
        self._reconnect_state: bool = False
        self._connection_time: float

        self._callbacks: Dict[str, Callable] = {
                "ping": self._ping
                }

        self._call_tasks: Set[Task] = set()
        self._calls: Dict[str, Union[dict, None]] = {}


        try:
            # Enable uvloop if available.
            tune()

        except NameError:
            pass


    @property
    def connected(self) -> bool:
        """Returns the connection status.

        :return: `True` if connected, else `False`.
        :rtype: bool
        """

        return not self._writer.is_closing()

    
    def callback(self, name: str) -> Callable:
        """Decorator to bind functions to be called when a request is received.

        :param name: Name to bind the function.
        :type name: str
        """

        assert name != "ping", "Name 'ping' is used internally."

        def decorator(function: Callable) -> Callable:
            self._callbacks.update({name: function})
            
            def wrapper(instance: Union[str, None], data: dict) -> Callable: # pylint: disable=unused-argument
                return function(instance, data)

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


    async def call(
            self,
            name: str,
            data: Optional[dict] = None,
            instance: Optional[str] = None,
            wait: bool = True,
            wait_timeout: int = 3,
            _call_id: Optional[str] = None
            ) -> Union[dict, bool, Exception, None]:
        """Calls a function in the server.

        :param name: Name of the function.
        :type name: str
        :param data: Data to send, defaults to `None`.
        :type data: dict
        :param instance: Instance to pass to the remote function, defaults to `None`.
        :type instance: Optional[str]
        :param wait: `True` to wait for a answer, defaults to `True`.
        :type wait: bool
        :param wait_timeout: Time limit in seconds to wait for a answer, defaults to `3`.
        :type wait_timeout: int
        :return: The call result.
        :rtype: Union[dict, bool, Exception, None]
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
            self._calls.update({call_id: None})

            datap.update({"call_id": call_id})
 
        
        try:
            dataf: bytes = b64encode(json.dumps(datap).encode("ascii")) + b"&"

            if not self._writer.is_closing():
                self._writer.write(dataf)
                await self._writer.drain()

        except (SyntaxError, RuntimeError, TypeError,
                ValueError, AssertionError, ConnectionError) as error:

            return error

        
        if to_wait:
            start_t: float = time()
            
            # Wait for a answer.
            while self._calls[call_id] is None and (time() - start_t) < wait_timeout:
                await sleep(0.01)

            # If was not answered returns None.
            if self._calls[call_id] is None:
                del self._calls[call_id]
                return None
            
            # If was answered returns the response.
            answer: dict = self._calls[call_id] # type: ignore
            del self._calls[call_id]
            return answer
        
        return True


    async def start(self) -> None:
        """Starts the client."""

        if self._ssl_context is not None:
            ssl_data = {
                    "ssl": self._ssl_context,
                    "ssl_handshake_timeout": self._connection_timeout*2
                    }

        else:
            ssl_data = {}


        if self._dlocal_host is None or self._dlocal_port is None:
            self._reader, self._writer = await open_connection( # type: ignore
                    host=self._host,
                    port=self._port,
                    limit=self._buffer_limit,
                    **ssl_data) # type: ignore

        # Binds to a specific local host and port.
        else:
            self._reader, self._writer = await open_connection( # type: ignore
                    host=self._host,
                    port=self._port,
                    local_addr=(self._dlocal_host, self._dlocal_port),
                    limit=self._buffer_limit,
                    **ssl_data) # type: ignore

        self._logger.info("Client | Connected to %s:%s", self._host, self._port)


        self._connection_time = time()

        if not self._reconnect_state:
            self._ping_task = create_task(self._ping_server())
            self._client_task = create_task(self._connection_handler())
            self._reconnect_state = True

        
    async def stop(self) -> None:
        """Stops the client."""

        self._ping_task.cancel()
        self._client_task.cancel()
        self._writer.close()

        self._reconnect_state = False
        self._connection_time = 0

    
    async def _ping_server(self) -> None:
        """Continuously check the connection status of the server."""

        while 1:
            current_time = time()

            # Checks if the connection is closed or if the server stop responding.
            if self._writer.is_closing() or ((current_time - self._connection_time) >= self._connection_timeout):
                if not self._writer.is_closing():
                    self._writer.close()

                self._connection_time = 0

                self._logger.info("Client | Disconnected from %s:%s", self._host, self._port)

                # Will keep trying to reconnect in case of disconnection.
                while self._reconnect and not self._connection_time:
                    self._logger.info("Client | Trying to reconnect to %s:%s", self._host, self._port)
                    
                    try:
                        await self.start()

                    except ConnectionError:
                        await sleep(self._reconnect_timeout)

                    else:
                        break
            
            # Ping the server.
            else:
                await self.call(name="ping", wait=False)

            await sleep(self._ping_timeout)
    
    
    async def _ping(self, instance: None, data: dict) -> None: # pylint: disable=unused-argument
        """Called when a ping is received from the server."""

        self._connection_time = time()
            

    async def _connection_handler(self) -> None:
        recv_data: bytes
        raw_data: str
        data: dict
        
        call: str
        call_id: Union[str, None]
        instance: str
        task: Task

        
        async def reset_buffer(timeout: float = 0) -> None:
            try:
                del recv_data, raw_data, data, call, call_id, instance, task

            except NameError:
                pass

            await sleep(timeout)


        while 1:
            try:
                try:
                    recv_data = await self._reader.readuntil(b"&")

                except LimitOverrunError:
                    self._logger.info("Client | Buffer limit exceeded")

                    await reset_buffer(0.1)
                    continue

                except (IncompleteReadError, ConnectionError):
                    await reset_buffer(0.1)
                    continue


                raw_data = b64decode(recv_data[:-1].decode("ascii")) # type: ignore
                data = json.loads(raw_data)


                if "call_id" in data:
                    call_id = data.pop("call_id")
                    
                    # Checks if the data is a answer of a previous call.
                    if call_id in self._calls:
                        del data["call"]
                        del data["instance"]

                        self._calls[call_id] = data

                        await reset_buffer()
                        continue

                else:
                    call_id = None


                call = data.pop("call")
                instance = data.pop("instance")


                if call in self._callbacks:
                    task = create_task(self._callbacks[call](instance, data))
                    
                    setattr(task, "call_id", call_id)
                    setattr(task, "call_name", call)
                    setattr(task, "call_instance", instance)

                    self._call_tasks.add(task)
                    task.add_done_callback(self._on_call_exit)

                elif "*" in self._callbacks:
                    task = create_task(self._callbacks["*"](instance, data))
                    
                    setattr(task, "call_id", call_id)
                    setattr(task, "call_name", call)
                    setattr(task, "call_instance", instance)

                    self._call_tasks.add(task)
                    task.add_done_callback(self._on_call_exit)

                
            except (json.JSONDecodeError, BinError, KeyError, TypeError,
                    ValueError, UnicodeDecodeError) as error:

                self._logger.error("Client | Error in the data received (%s)", error)

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
                    wait=False,
                    _call_id=task.call_id # type: ignore
                    ))

                self._call_tasks.add(rtask)
                rtask.add_done_callback(self._call_tasks.discard)

            except AssertionError:
                pass

        self._call_tasks.discard(task)
