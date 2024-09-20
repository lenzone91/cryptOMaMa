# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import time
import datetime as dt
import json
import os
from threading import Thread
from binance import ThreadedWebsocketManager
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Stream():
        
    def get_historical_datas(self, api_key : str, private_key : str, symbol : str, output_file_name : str, duration : int):
        """
        Open a stream with Binance to get useful datas for model calibration.
        Save datas in a .txt file

        Parameters
        ----------
        api_key : str
            Public api key for Binance
        private_key : str
            Path to the pem file that contains private api key for Binance
        symbol : str
            Pair symbol (e.g 'BTCUSDT') 
        output_file_name : str
            Path to the output file that will contains historical datas
        duration : int
            Stream duration (in seconds)
        """

        self.stream_error = False
        self.api_key = api_key
        self.private_key = private_key
        self.output_file_name = output_file_name

        # remove existing file : 
        if os.path.isfile(output_file_name) :
            os.remove(output_file_name)

        with open(private_key, 'rb') as key_file:
                private_key = load_pem_private_key(data = key_file.read(), password = None)

        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=private_key)
        # start is required to initialise its internal loop
        self.twm.start()
        
        self.streams = [symbol.lower() + '@depth5@100ms', symbol.lower() + '@bookTicker', symbol.lower() + '@trade']
        
        self.twm.start_multiplex_socket(callback = self.handle_socket_message, streams = self.streams)
        
        stop_trades = Thread(target = self.restart_stream, daemon = True)
        stop_trades.start()

        start = dt.datetime.now()
        end = start + dt.timedelta(seconds=duration)

        while dt.datetime.now() < end : 
            pass

        self.twm.stop()
    
    def handle_socket_message(self, msg):
            #print(f"message type: {msg['e']}")
            print(msg)
            if 'data' in msg :
                with open(self.output_file_name, "a") as file:
                    json.dump(msg, file)
                    file.write("\n")
            else : 
                self.stream_error = True

    def restart_stream(self):
        while True:
            if self.stream_error == True:
                self.twm.stop()
                self.stream_error = False
                self.twm = ThreadedWebsocketManager(api_key=self.api_key, api_secret=self.private_key)
                self.twm.start()
                self.twm.start_multiplex_socket(callback = self.handle_socket_message, streams = self.streams)
