# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import os
import shutil
import time

from .model_tools.model_utils import create_model
from .api_tools import api_utils
from .calibration_tools import calibration


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
        if args.historical_dir : 
            self.historical_dir = args.historical_dir
        if args.model:
            self.model = create_model(args.model)
        if self.use_api :
            try : 
                self.api = args.api
                self.duration = args.duration
                self.api_key = args.api_key
                self.private_key = args.private_key
                self.broker = api_utils.create_broker(self.api, self.api_key, self.private_key, self.historical_dir)
            except Exception as e:
                print("Terminated unsuccessfully")
                raise Exception("Terminated unsuccessfully") from e
    def launch(self):
        """
        Launch the execution of the model with the specified broker or input datas.
        """
        if self.CMD == "run":
            
            if self.use_api :
                # remove existing file : 
                if os.path.isdir(self.historical_dir) :
                    shutil.rmtree(self.historical_dir)

                broker = api_utils.create_broker("binance", self.api_key, self.private_key, self.historical_dir)
                broker.launch_websocket_in_thread(self.symbol)
                time.sleep(self.duration)
            while 1:
                calibration.transaction_intensity(self.historical_dir)
                print("")
            quotes = self.model.compute_quotes(True,1,1,10,1,1,1,0)
            print(quotes)



