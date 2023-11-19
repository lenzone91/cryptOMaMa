"""
Broker class test
"""

import unittest
from src.api_tools.broker import Broker

class TestBroker(unittest.TestCase):
    """
    Broker class test
    """

    def test_post_request(self):
        """
        Testing of post request TypeError
        """
        # Ensure the post_request method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().post_request()

    def test_get_request(self):
        """
        Testing of get request TypeError
        """
        # Ensure the get_request method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_request()

    def test_get_avg_price(self):
        """
        Testing of get average price request TypeError
        """
        # Ensure the get_avg_price method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_avg_price('BTCUSDT')

    def test_ping(self):
        """
        Testing of ping request TypeError
        """
        # Ensure the ping method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().ping()

    def test_get_depth(self):
        """
        Testing of get depth request TypeError
        """
        # Ensure the get_depth method is abstract and raises TypeError
        with self.assertRaises(TypeError):
            Broker().get_depth('BTCUSDT')

if __name__ == '__main__':
    unittest.main()
