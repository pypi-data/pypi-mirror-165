import asyncio
import functools
import json
import os
import pandas as pd
import requests
import websockets

from typing import Callable, Coroutine


def function_endpoint(environment: str = 'dev', api_key: str = 'public'):
    if environment == 'prod':
        url_base = 'wss://ws.finx.io/streamer/' + api_key
    elif environment == 'dev':
        url_base = 'wss://beta.finx.io/streamer/' + api_key
    elif environment == 'prod_rest':
        url_base = 'https://ws.finx.io/backend/'
    elif environment == 'dev_rest':
        url_base = 'https://beta.finx.io/backend/'
    else:
        url_base = ''
    return url_base


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


class TickPlant:

    def __init__(self, finx_api_key: str = 'public', environment: str = "dev"):
        self.api_key = finx_api_key or os.getenv('FINX_API_KEY')
        self.endpoint = function_endpoint(environment, self.api_key)
        self.rest_endpoint = function_endpoint(environment + '_rest')
        print('-----> TickPlant initialized -----> ')
        print('-----> user: ' + finx_api_key + ' -----> ')

    async def __aenter__(self):
        print('-----> Python SDK Connecting ----->')
        print('-----> endpoint: ' + self.endpoint + ' ----->')
        self._conn = websockets.connect(self.endpoint)
        self.websocket = await self._conn.__aenter__()
        is_auth = await self._authenticate()
        print('-----> FinX API Key authenticated -----> ', is_auth)
        result = await self._dispatch(dict(APIKey=self.api_key, pair='BTC:USDC', functionName='tickSnap'))
        print('TickPlant connection test:', result)
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
        print(self.websocket)
        return await self.__receive()

    @Hybrid
    async def _authenticate(self) -> dict:
        is_auth = await self._dispatch(dict(
            APIKey=self.api_key,
            functionName='authenticate'
        ))
        return is_auth

    @Hybrid
    async def get_reference_data(self, ticker: str) -> dict:
        return await self._dispatch(dict(securityId=ticker, functionName='referenceData'))

    @Hybrid
    async def list_deribit_contracts(self) -> dict:
        return await self._dispatch(dict(functionName='listDeribitContracts'))

    @Hybrid
    async def tick_snap(self, pair, unix_time_target='', time_target_width_seconds='') -> dict:
        if not pair:
            return str('missing "pair" parameter')
        url_string = self.rest_endpoint + \
                     'observations/tick/snap' \
                     '?APIKey=' + self.api_key + \
                     '&pair=' + pair
        if unix_time_target:
            url_string += '&unixTimeTarget='+unix_time_target
            if time_target_width_seconds:
                url_string += '&timeTargetWidthSeconds='+time_target_width_seconds
            else:
                url_string += '&timeTargetWidthSeconds=10'
        print('url_string', url_string)
        response = requests.get(url_string).json()

        return response

    @Hybrid
    async def tick_history(self, pair: str, date: str, time: str = "00:00") -> dict:
        return await self._dispatch(dict(
            pair=pair,
            date=date,
            time=time,
            functionName='tickHistory'))

    @Hybrid
    async def get_timeslice(self, timeslice_datestamp, timeslice_width_seconds, underlying_symbol) -> pd.DataFrame:
        url_string = self.rest_endpoint + \
                     'observations/options/time_slice' \
                     '?APIKey=' + self.api_key + \
                     '&timeslice_target_datestamp=' + timeslice_datestamp + \
                     '&timeslice_width_seconds=' + timeslice_width_seconds + \
                     '&underlying_symbol=' + underlying_symbol
        response = requests.get(url_string)
        df = pd.DataFrame(response.json())
        return df

    @Hybrid
    async def get_timeslice_series(self, api_key, series_start_datestamp, series_end_datestamp, series_step_seconds, timeslice_width_seconds, underlying_symbol) -> pd.DataFrame:
        number_of_periods = int((int(series_end_datestamp) - int(series_start_datestamp)) / int(series_step_seconds))
        print('running time series of timeslices with ' + str(number_of_periods) + ' periods from ' + str(series_start_datestamp) + ' to ' + str(series_end_datestamp))
        for i in range(number_of_periods):
            timeslice_datestamp = int(series_start_datestamp) + (i*int(series_step_seconds))
            this_frame = await self.get_timeslice(api_key, str(timeslice_datestamp), str(timeslice_width_seconds), underlying_symbol)
            print('this_frame:'+str(i), this_frame)
            if i == 0:
                return_df = this_frame
            else:
                if len(this_frame) > 0:
                    return_df = pd.concat([return_df, this_frame], ignore_index=True)
        return return_df

    @Hybrid
    async def connect(self):
        await self.__aenter__()
