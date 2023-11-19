import unittest
from unittest.mock import patch, mock_open
from argparse import Namespace
from src.utils.args_reading import *

class Test_Args_Reading(unittest.TestCase):

    def test_process_inputs_from_json(self):
        # Mocking input arguments and file content for the test
        args = Namespace(input_file='test.json', api=None, api_key=None, private_key=None, symbol=None, model=None)
        mock_file_content = '{"use_api": {"api": "binance","api_key": "key_test","private_key": "Private_key_path","symbol": "BTCUSDT"},\
                            "model": "GueantLehalleFernandezTapia"}'
        expected_result = Namespace(input_file='test.json', api='binance', api_key="key_test", private_key="Private_key_path", symbol="BTCUSDT", model="GueantLehalleFernandezTapia")

        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            result = process_inputs_from_json(args)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
