# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import os
from ..broker import Broker
from threading import Thread
import json
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient


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

    def __init__(self, api_key: str, private_key: str, historical_dir : str):
        super().__init__("Binance")
        self.api_key = api_key
        self.private_key = private_key
        self.historical_dir = historical_dir

    #WEBSOCKET PART

    def message_handler(self, _, msg):
        print(msg)
        if 'data' in msg :
            if "depth20" in msg : 
                file = "depth20.txt"
            elif "aggTrade" in msg : 
                file = "aggTrade.txt"
            elif "depth" in msg : 
                file = "depth.txt"
            if not os.path.isdir(self.historical_dir):
                os.mkdir(self.historical_dir)
            with open(os.path.join(self.historical_dir,file), "a") as file:
                json.dump(json.loads(msg)["data"], file)
                file.write("\n")
        
    def open_web_socket(self, symbol):
        my_client = SpotWebsocketStreamClient(on_message=self.message_handler, is_combined=True)

        # Subscribe to a single symbol stream
        my_client.subscribe(stream=[symbol.lower()+"@depth@100ms", symbol.lower()+"@aggTrade", symbol.lower()+"@depth20@100ms"])

    def launch_websocket_in_thread(self, symbol):

        thread = Thread(target=self.open_web_socket, args=(symbol,))
        thread.start()
    
