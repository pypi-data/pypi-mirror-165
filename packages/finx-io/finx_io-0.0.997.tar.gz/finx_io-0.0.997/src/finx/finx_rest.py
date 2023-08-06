import asyncio
import datetime
import calendar
import functools
import json
import os
import pandas as pd
import requests
import time
import websockets
from typing import Callable, Coroutine

def function_endpoint(environment: str = 'dev', api_key: str = 'public'):
    if environment == 'prod':
        url_base = 'wss://prod.finx.io/streamer/' + api_key
    elif environment == 'dev':
        url_base = 'wss://beta.finx.io/streamer/' + api_key
    elif environment == 'prod_rest':
        url_base = 'https://prod.finx.io/backend/'
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


class FinXRest:

    def __init__(self, finx_api_key: str = 'public', environment: str = "dev"):
        self.api_key = finx_api_key or os.getenv('FINX_API_KEY')
        self.endpoint = function_endpoint(environment, self.api_key)
        self.rest_endpoint = function_endpoint(environment + '_rest')
        print('-----> FinXRest Client Initialized -----> ')
        print('-----> user: ' + finx_api_key + ' -----> ')

    async def __aenter__(self):
        print('-----> Python SDK Connecting ----->')
        print('-----> endpoint: ' + self.endpoint + ' ----->')
        self._conn = websockets.connect(self.endpoint)
        self.websocket = await self._conn.__aenter__()
        is_auth = await self._authenticate()
        print('-----> FinX API Key authenticated -----> ', is_auth)
        #TODO: update the connection checker to a check_connection function
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
    async def get_reference_data(self, security_id: str, unix_time: str = None) -> dict:
        url_string = self.rest_endpoint + \
                     'reference/secdb' \
                     '?APIKey=' + self.api_key + \
                     '&securityId=' + security_id
        response = requests.get(url_string).json()
        return response

    @Hybrid
    async def list_deribit_contracts(self) -> list:
        url_string = self.rest_endpoint + \
                     'deribit/list-deribit-contracts' \
                     '?APIKey=' + self.api_key
        response = requests.get(url_string).json()
        return response

    @Hybrid
    async def list_pairs(self) -> list:
        url_string = self.rest_endpoint + 'observations/pairs' + '?APIKey=' + self.api_key
        response = requests.get(url_string).json()
        return response

    @Hybrid
    async def pair_quote(self, pair, unix_time_target='', time_target_width='') -> dict:
        if not pair:
            return str('missing "pair" parameter')
        url_string = self.rest_endpoint + \
                     'observations/tick/snap' \
                     '?APIKey=' + self.api_key + \
                     '&pair=' + pair
        if unix_time_target:
            url_string += '&unixTimeTarget='+unix_time_target
            if time_target_width:
                url_string += '&timeTargetWidthSeconds='+time_target_width
            else:
                url_string += '&timeTargetWidthSeconds=10'
        response = requests.get(url_string).json()
        return response

    @Hybrid
    async def pair_quote_series(self, pair: str, unix_time_start: str,  unix_time_end: str, timeslice_width_seconds:str) -> pd.DataFrame:
        number_of_periods = 100
        distance_between_periods = (int(unix_time_end) - int(unix_time_start)) / number_of_periods
        print('running time series of pair quotes with ' + str(number_of_periods) + ' periods from ' + str(unix_time_start) + ' to ' + str(unix_time_end))
        for i in range(number_of_periods):
            timeslice_datestamp = int(unix_time_start) + (i*distance_between_periods)
            this_frame = await self.pair_quote(pair, str(timeslice_datestamp), timeslice_width_seconds)
            print('this_frame:'+str(i), this_frame)
            if i == 0:
                return_df = pd.DataFrame.from_records([this_frame])
            else:
                try:
                    if len(this_frame) > 0:
                        add_df = pd.DataFrame.from_records([this_frame])
                        return_df = pd.concat([return_df, add_df], ignore_index=True)
                except:
                    continue
        return_df['datetime'] = return_df['unix_time'].to_datetime()
        return_df['price'] = return_df['price'].astype(float)
        return return_df

    @Hybrid
    async def get_options_timeslice(self, timeslice_datestamp, timeslice_width_seconds, underlying_symbol) -> pd.DataFrame:
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
    async def get_options_timeslice_series(self, unix_time_start, unix_time_end, timeslice_width_seconds, underlying_symbol) -> pd.DataFrame:
        number_of_periods = int((int(unix_time_end) - int(unix_time_start)) / int(unix_time_end))
        print('running time series of timeslices with ' + str(number_of_periods) + ' periods from ' + str(unix_time_start) + ' to ' + str(unix_time_end))
        for i in range(number_of_periods):
            timeslice_datestamp = int(unix_time_start) + (i*int(unix_time_end))
            this_frame = await self.get_options_timeslice(str(timeslice_datestamp), str(timeslice_width_seconds), underlying_symbol)
            print('this_frame:'+str(i), this_frame)
            if i == 0:
                return_df = this_frame
            else:
                if len(this_frame) > 0:
                    return_df = pd.concat([return_df, this_frame], ignore_index=True)
        return return_df

    def _calc_years_to_expiry(self, row):
        print("row", row)
        instrument_name = row['instrument_name']
        years_to_expiry = 0.0
        day_value = instrument_name.split("-")[1][0:2]
        month_value = instrument_name.split("-")[1][2:5]
        year_value = instrument_name.split("-")[1][5:8]
        date_string = year_value + '/' + month_value + '/' + day_value
        expiry_unix = datetime.datetime.strptime(date_string, '%y/%b/%d').timestamp()
        years_to_expiry = (expiry_unix - time.time()) / 60 / 60 / 24 / 365
        return years_to_expiry

    def _parse_strike_price(self, row):
        return row['instrument_name'].split("-")[2]

    @Hybrid
    async def prepare_vol_surface_inputs(self, filename, timeslice_datestamp, timeslice_width_seconds, underlying_symbol) -> str:
        df = pd.DataFrame(await self.get_options_timeslice(timeslice_datestamp, timeslice_width_seconds, underlying_symbol))
        print('vol_surface_inputs raw:', df)
        df['years_to_expiry'] = df.apply(lambda row: self._calc_years_to_expiry(row), axis=1)
        df['strike_price'] = df.apply(lambda row: self._parse_strike_price(row), axis=1)
        output_df = df[['years_to_expiry', 'strike_price', 'mark_iv']]
        output_df.rename(columns={"years_to_expiry": "expiration", "strike_price": "price", "mark_iv": "price"})
        # must be expiration,strike,price
        #,redis_key,underlying_price,underlying_index,timestamp,state,settlement_price,open_interest,min_price,max_price,mark_price,mark_iv,last_price,interest_rate,instrument_name,index_price,estimated_delivery_price,bid_iv,best_bid_price,best_bid_amount,best_ask_price,best_ask_amount,ask_iv,vega,theta,rho,gamma,delta,volume,price_change,low,high
        output_df.to_csv(filename, index=False)
        return filename

    @Hybrid
    async def connect(self):
        await self.__aenter__()

