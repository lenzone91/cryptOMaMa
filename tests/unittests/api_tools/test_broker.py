import unittest
from abc import ABC, abstractmethod
from src.api_tools.broker import Broker

class TestBroker(unittest.TestCase):

    def test_post_request(self):
        # Ensure the post_request method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().post_request()

    def test_get_request(self):
        # Ensure the get_request method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_request()

    def test_get_avgPrice(self):
        # Ensure the get_avgPrice method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_avgPrice('BTCUSDT')

    def test_ping(self):
        # Ensure the ping method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().ping()

    def test_get_depth(self):
        # Ensure the get_depth method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_depth('BTCUSDT')

if __name__ == '__main__':
    unittest.main()
