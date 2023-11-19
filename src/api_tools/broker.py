"""
Abstract base class for Brokers
"""

from abc import ABC, abstractmethod

class Broker(ABC):
    """
    Abstract base class for Brokers
    """

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
        
