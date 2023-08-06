import asyncio
import functools
import json
import os
import websockets

from typing import Callable, Coroutine

def streamer_endpoint(params, environment: str = None):
    if environment == 'dev':
        return 'wss://beta.finx.io/streamer/'+params["api_key"]+'/'+params["pair"]
    return 'wss://ws.finx.io/streamer/'+params["api_key"]+'/'+params["pair"]

def task_runner(task: Coroutine):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    run_loop = (loop.is_running() and loop.create_task) or loop.run_until_complete
    try:
        return run_loop(task)
    except TypeError:
        raise Exception('BAD LOOP PARAMS')


class Hybrid:

    def __init__(self, func: Callable):
        self._func = func
        self._func_name = func.__name__
        self._func_path = func.__name__
        self._func_class = None
        functools.update_wrapper(self, func)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        self._func_class = obj
        return self

    def __call__(self, *args, **kwargs):
        return task_runner(self.run_func(*args, **kwargs))

    async def run_func(self, *args, **kwargs):
        if self._func_class is not None:
            args = (self._func_class,) + args
        return await self._func(*args, **kwargs)

    async def run_async(self, *args, **kwargs):
        return await self.run_func(*args, **kwargs)


def read_stream(conn):
    while True:
        try:
            result = conn.recv()
            print(result)
        except Exception as e:
            print(e)
            break

class Streamer:

    def __init__(self, payload, environment: str = "dev"):
        self.api_key = os.getenv('FINX_API_KEY')
        self.pair = payload['pair']
        self.endpoint = streamer_endpoint(dict(api_key=self.api_key, pair=self.pair), environment)
        print('-----> Streamer initialized -----> ')

    async def __aenter__(self):
        print('-----> Python SDK Connecting ----->')
        self._conn = websockets.connect(self.endpoint)
        self.websocket = await self._conn.__aenter__()
        is_auth = await self._authenticate()
        print('-----> FinX API Key authenticated -----> ', is_auth)
        result = await self._dispatch(dict(message="message"))
        print('Streamer connection test', result)
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def __send(self, message: dict):
        message.update(APIKey=self.api_key)
        await self.websocket.send(json.dumps(message))

    async def __receive(self):
        return await self.websocket.recv()

    async def _dispatch(self, message: dict):
        await self.__send(message)
        return await self.__receive()

    @Hybrid
    async def _authenticate(self) -> dict:
        is_auth = await self._dispatch(dict(
            APIKey=self.api_key,
            functionName='authenticate'
        ))
        return is_auth

    @Hybrid
    async def listen(self, output='console'):
        if output != 'console':
            output_file = open(output,"w")
            print('writing to file:', output)
        else:
            print('writing to ', output)
        while True:
            try:
                response = await self._dispatch(dict(message=dict(pair=self.pair)))
            except self._conn.__aexit__:
                break
            if output=='console':
                print(response)
            else:
                output_file.writelines(response)
                output_file.writelines("\n")

    @Hybrid
    async def connect(self):
        await self.__aenter__()
