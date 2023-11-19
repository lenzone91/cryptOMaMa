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
        pass

    @abstractmethod
    def get_request(self):
        """
        Abstract method for handling GET requests.
        """
        pass

    @abstractmethod
    def get_avgPrice(self, symbol):
        """
        Abstract method for getting average price.
        """
        pass

    @abstractmethod
    def ping(self):
        """
        Abstract method for handling ping requests.
        """
        pass

    @abstractmethod
    def get_depth(self, symbol):
        """
        Abstract method for getting depth information.
        """
        pass
