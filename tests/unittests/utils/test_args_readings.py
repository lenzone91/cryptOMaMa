"""
Args reading methods test
"""

import unittest
from unittest.mock import patch, mock_open
from argparse import Namespace
from src.utils.args_reading import process_inputs_from_json

class TestArgsReading(unittest.TestCase):
    """
    Args reading methods test
    """

    def test_process_inputs_from_json(self):
        """
        Testing the inputs from json file
        """
        # Mocking input arguments and file content for the test
        args = Namespace(input_file='test.json', api=None, api_key=None,\
                         private_key=None, symbol=None, model=None)
        mock_file_content = '{"use_api": {"api": "binance",\
                                          "api_key": "key_test",\
                                          "private_key":\
                                          "Private_key_path",\
                                          "symbol": "BTCUSDT"},\
                              "model": "process_inputs_from_json"}'
        expected_result = Namespace(input_file='test.json', api='binance',\
                                    api_key="key_test", private_key="Private_key_path",\
                                    symbol="BTCUSDT", model="process_inputs_from_json")

        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            result = process_inputs_from_json(args)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
