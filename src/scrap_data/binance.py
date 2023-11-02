import requests
import base64
import time
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Binance():
    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key_path = private_key
        self.params = {}
        self.url = 'https://api.binance.com/api/v3/'
        self.headers = {
            'X-MBX-APIKEY': self.api_key,
        }

    def send_request(self):
        
        with open(self.private_key_path, 'rb') as f:
            self.private_key = load_pem_private_key(data=f.read(),password=None)
            
        #timestamp = int(time.time() * 1000)
        #self.params['timestamp'] = timestamp

        # Sign the request
        payload = '&'.join([f'{param}={value}' for param, value in self.params.items()])
        signature = base64.b64encode(self.private_key.sign(payload.encode('ASCII')))
        self.params['signature'] = signature

        # Send the request
        response = requests.post(
            self.url+self.request_type,
            headers=self.headers,
            data=self.params,
        )
        print(response.json())
        return response.json()
    
    def get_avgPrice(self, symbol):
        self.request_type = "avgPrice"
        self.params = {
            'symbol': symbol
        } 
        return self.send_request()
    
    def get_ping(self):
        self.request_type = "ping"
        self.params = {} 
        return self.send_request()