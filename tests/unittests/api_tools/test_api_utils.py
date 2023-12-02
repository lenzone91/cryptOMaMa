# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import unittest
from unittest.mock import patch
from src.api_tools.api_utils import create_broker

class TestCreateBroker(unittest.TestCase):
    """
    API utils class test
    """

    @patch('src.api_tools.api_utils.Binance')
    def test_create_broker_binance(self, mock_binance):
        """
        Testing of Binance object creation
        """
        # Mock the Binance class
        mock_binance_instance = mock_binance.return_value

        # Call the create_broker function with "binance"
        result = create_broker(api="binance", api_key="mock_api_key",\
                               private_key="mock_private_key")

        # Assert that the Binance constructor was called with the expected positional arguments
        mock_binance.assert_called_once_with("mock_api_key", "mock_private_key")

        # Assert that the result is the mocked Binance instance
        self.assertEqual(result, mock_binance_instance)


    @patch('src.api_tools.api_utils.Binance')
    def test_create_broker_invalid_type(self, mock_binance):
        """
        Testing of object creation with invalid_type
        """

        # Call the create_broker function with an unsupported type
        with self.assertRaises(ValueError) as context:
            create_broker(api="invalid_type", api_key="mock_api_key",\
                          private_key="mock_private_key")

        # Assert that the ValueError is raised with the expected message
        self.assertEqual(str(context.exception), "Unsupported broker type: invalid_type")

        # Assert that the Binance constructor was not called
        mock_binance.assert_not_called()

if __name__ == '__main__':
    unittest.main()
