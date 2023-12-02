# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

from abc import ABC, abstractmethod

class Broker(ABC):
    """
    Abstract base class for brokers
    """
    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def post_request(self):
        """
        Abstract method for handling POST requests.
        """

    @abstractmethod
    def get_request(self):
        """
        Abstract method for handling GET requests.
        """

    @abstractmethod
    def get_avg_price(self, symbol):
        """
        Abstract method for getting average price.
        """

    @abstractmethod
    def ping(self):
        """
        Abstract method for handling ping requests.
        """

    @abstractmethod
    def get_depth(self, symbol):
        """
        Abstract method for getting depth information.
        """
