from abc import ABC, abstractmethod

class Broker(ABC):
    
    @abstractmethod
    def post_request(self):
        pass

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_avgPrice(self, symbol):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def get_depth(self, symbol):
        pass




