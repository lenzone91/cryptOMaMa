# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

from src.model_tools.model_utils import create_model
from src.api_tools import api_utils

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
        self.mode = args.mode
        self.api = args.api
        self.api_key = args.api_key
        self.private_key = args.private_key
        self.symbol = args.symbol
        self.model = create_model(args.model)
        if self.api :
            self.broker = api_utils.create_broker(self.api, self.api_key, self.private_key)

    def launch(self):
        """
        Launch the execution of the model with the specified broker or input datas.
        """
        if self.mode == "run":
            if self.api :
                response = self.broker.get_avg_price(self.symbol)
                print(response)
            quotes = self.model.compute_quotes(True,1,1,10,1,1,1,0)
            print(quotes)
