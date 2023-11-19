import unittest
from unittest.mock import patch
from src.api_tools.brokers.binance import Binance
import numpy as np

class TestBinance(unittest.TestCase):

    def setUp(self):
        # Mock the API key and private key for testing
        self.mock_api_key = "mock_api_key"
        self.mock_private_key = "mock_private_key"

    @patch('src.api_tools.brokers.binance.Binance.get_request')
    def test_get_avgPrice(self, mock_get_request):
        # Create a Binance instance
        binance = Binance(self.mock_api_key, self.mock_private_key)

        # Mock the get_request method
        mock_get_request.return_value = {'avgPrice': '123.45'}

        # Call the get_avgPrice method
        result = binance.get_avgPrice('BTCUSDT')

        # Assert that the get_request method was called with the expected parameters
        mock_get_request.assert_called_once()

        # Assert that the result is the expected average price
        self.assertEqual(result, {'avgPrice': '123.45'})

    @patch('src.api_tools.brokers.binance.Binance.get_request')
    def test_ping(self, mock_get_request):
        # Create a Binance instance
        binance = Binance(self.mock_api_key, self.mock_private_key)

        # Mock the get_request method
        mock_get_request.return_value = {'status': 'pong'}

        # Call the ping method
        result = binance.ping()

        # Assert that the get_request method was called with the expected parameters
        mock_get_request.assert_called_once()

        # Assert that the result is the expected ping response
        self.assertEqual(result, {'status': 'pong'})

    @patch('src.api_tools.brokers.binance.Binance.get_request')
    def test_get_depth(self, mock_get_request):
        # Create a Binance instance
        binance = Binance(self.mock_api_key, self.mock_private_key)

        # Mock the get_request method
        mock_get_request.return_value = {'bids': [['10.00', '5'], ['9.99', '10']], 'asks': [['10.05', '8'], ['10.10', '12']]}

        # Call the get_depth method
        bids, asks = binance.get_depth('BTCUSDT')
        
        # Assert that the get_request method was called with the expected parameters
        mock_get_request.assert_called_once()

        # Assert that the bids and asks are the expected arrays using numpy.testing.assert_array_equal
        np.testing.assert_array_equal(bids, np.array([['10.00', '5'], ['9.99', '10']]))
        np.testing.assert_array_equal(asks, np.array([['10.05', '8'], ['10.10', '12']]))

if __name__ == '__main__':
    unittest.main()
