# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import base64
import time
import requests
import numpy as np
import pandas as pd
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from ..broker import Broker


class Binance(Broker):
    """
    Implementation of the Broker interface for Binance.

    Notes
    -----
    More details on the Binance API at : 
    https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints

    Parameters
    ----------
    api_key : str
        public api key for Binance
    private_key : str
        private api key for Binance

    Methods
    -------
    post_request()
        Post a request
    get_request()
        Get a request
    get_avg_price()
        Get the average price of a symbol
    ping()
        Send a ping to the API server to check the connection
    get_depth()
        Get the available order book orders on the market for a symbol 
    """

    def __init__(self, api_key: str, private_key: str):
        super().__init__("Binance")
        self.api_key = api_key
        self.private_key = private_key
        self.params = {}
        self.url = 'https://api.binance.com/api/v3/'
        self.headers = {
            'X-MBX-APIKEY': self.api_key,
        }
        self.request_type = ""

    def post_request(self):
        """
        Implement the post_request method for Binance.
        """
        with open(self.private_key, 'rb') as key_file:
            self.private_key = load_pem_private_key(data=key_file.read(),password=None)

        timestamp = int(time.time() * 1000)
        self.params['timestamp'] = timestamp

        payload = '&'.join([f'{param}={value}' for param, value in self.params.items()])
        signature = base64.b64encode(self.private_key.sign(payload.encode('ASCII')))
        self.params['signature'] = signature

        response = requests.post(
            self.url+self.request_type,
            headers=self.headers,
            data=self.params,
            timeout=60
        )
        print(response.json())
        return response.json()

    def get_request(self):
        """
        Implement the get_request method for Binance.
        """
        response = requests.get(
            self.url+self.request_type,
            params=self.params,
            timeout=60
        )
        return response.json()

    def get_avg_price(self, symbol: str):
        """
        Implement the get_avg_price method for Binance.
        Get the average price of a symbol

        Parameters
        ----------
        symbol : str
            Pair symbol (e.g 'BTCUSDT') 

        Returns
        -------
        request : dict
            {'mins' : Average price interval (in minutes),
             'price' : Average price,
             'closeTime' : Last trade time
            }
        """
        self.request_type = "avgPrice"
        self.params = {
            'symbol': symbol
        }
        return self.get_request()

    def ping(self):
        """
        Implement the ping method for Binance.
        Send a ping to the API server to check the connection
        """
        self.request_type = "ping"
        self.params = {}
        return self.get_request()

    def get_depth(self, symbol, limit=20):
        """
        Implement the get_depth method for Binance.
        Get the available order book orders on the market for a symbol 

        Parameters
        ----------
        symbol : str
            Pair symbol (e.g 'BTCUSDT') 
        limit : int
            Size of the wanted LOB. (20 at each side by default)

        Returns
        -------
        bids : np.array
            The actual n first bid limits [price_i, volume_i]
        asks : np.array
            The actual n first ask limits [price_i, volume_i] 
        """
        self.request_type = "depth"
        self.params = {
            'symbol': symbol,
            'limit': limit
        }
        response = self.get_request()
        bids = np.array(response["bids"])
        asks = np.array(response["asks"])
        return bids, asks
    
    def get_trades(self, symbol, limit=20):
        """
        Implement the get_trades method for Binance.
        Get the last trades on the market for a symbol 

        Parameters
        ----------
        symbol : str
            Pair symbol (e.g 'BTCUSDT') 
        limit : int
            Size of the historic. (20 by default)

        Returns
        -------
        Dict of 
        """
        self.request_type = "trades"
        self.params = {
            'symbol': symbol,
            'limit': limit
        }
        response = self.get_request()
        response = pd.DataFrame.from_dict(response)
        response["time"] = pd.to_datetime(response["time"], unit='ms')
        return response
