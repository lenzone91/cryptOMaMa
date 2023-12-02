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
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from ..broker import Broker

class Binance(Broker):
    """
    Implementation of the Broker interface for Binance.
    """

    def __init__(self, api_key, private_key):
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

    def get_avg_price(self, symbol):
        """
        Implement the get_avg_price method for Binance.
        """
        self.request_type = "avgPrice"
        self.params = {
            'symbol': symbol
        }
        return self.get_request()

    def ping(self):
        """
        Implement the ping method for Binance.
        """
        self.request_type = "ping"
        self.params = {}
        return self.get_request()

    def get_depth(self, symbol):
        """
        Implement the get_depth method for Binance.
        """
        self.request_type = "depth"
        self.params = {
            'symbol': symbol,
            'limit': 20
        }
        response = self.get_request()
        bids = np.array(response["bids"])
        asks = np.array(response["asks"])
        return bids, asks
