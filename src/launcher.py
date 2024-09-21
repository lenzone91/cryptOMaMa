# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

from .model_tools.model_utils import create_model
from .api_tools import api_utils
from .calibration_tools import calibration
from .api_tools.binance_cheat import Stream


class Launcher:
    """
    Launcher class for handling the execution of the model with a specified broker or input datas.
    """

    def __init__(self, args):
        """
        Initialize the Launcher instance.

        Args:
            args (Namespace): Command-line arguments.
        """
        self.CMD = args.CMD
        self.use_api = args.use_api
        self.symbol = args.symbol
        if args.historical_file : 
            self.historical_file = args.historical_file
        if args.model:
            self.model = create_model(args.model)
        if self.use_api :
            try : 
                self.api = args.api
                self.duration = args.duration
                self.api_key = args.api_key
                self.private_key = args.private_key
                self.broker = api_utils.create_broker(self.api, self.api_key, self.private_key)
            except Exception as e:
                print("Terminated unsuccessfully")
                raise Exception("Terminated unsuccessfully") from e
    def launch(self):
        """
        Launch the execution of the model with the specified broker or input datas.
        """
        if self.CMD == "test":
            # First step is to get datas from the broker
            if self.use_api :
                # Temporary method using python-binance for now
                my_stream = Stream()
                my_stream.get_historical_datas(self.api_key, self.private_key, self.symbol, self.historical_file, self.duration)
            # Second step is to calibrate model from datas
            calibration.transaction_intensity(self.historical_file)
            print(response)
            quotes = self.model.compute_quotes(True,1,1,10,1,1,1,0)
            print(quotes)
