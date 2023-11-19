import requests
import base64
import time
import numpy as np
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from src.api_tools.broker import Broker

class Binance(Broker):
    def __init__(self, api_key, private_key):
        super().__init__()
        self.api_key = api_key
        self.private_key = private_key
        self.params = {}
        self.url = 'https://api.binance.com/api/v3/'
        self.headers = {
            'X-MBX-APIKEY': self.api_key,
        }

    def post_request(self):
        
        with open(self.private_key_path, 'rb') as f:
            self.private_key = load_pem_private_key(data=f.read(),password=None)
            
        timestamp = int(time.time() * 1000)
        self.params['timestamp'] = timestamp

        payload = '&'.join([f'{param}={value}' for param, value in self.params.items()])
        signature = base64.b64encode(self.private_key.sign(payload.encode('ASCII')))
        self.params['signature'] = signature

        response = requests.post(
            self.url+self.request_type,
            headers=self.headers,
            data=self.params,
        )
        print(response.json())
        return response.json()
    
    def get_request(self):
        response = requests.get(
            self.url+self.request_type,
            params=self.params,
        )
        return response.json()
    
    def get_avgPrice(self, symbol):
        self.request_type = "avgPrice"
        self.params = {
            'symbol': symbol
        } 
        return self.get_request()
    
    def ping(self):
        self.request_type = "ping"
        self.params = {} 
        return self.get_request()
    
    def get_depth(self, symbol):
        self.request_type = "depth"
        self.params = {
            'symbol': symbol,
            'limit': 20
        }
        response = self.get_request()
        bids = np.array(response["bids"])
        asks = np.array(response["asks"])
        return bids, asks