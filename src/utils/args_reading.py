"""
Input arguments treatment
"""

import argparse
import json

def process_arguments():
    """
    Process command line arguments, including optional input file processing.
    """

    parser = create_parser()
    args = parser.parse_args()

    if args.input_file:
        args = process_inputs_from_json(args)
    return args

def create_parser():
    """
    Create an argument parser for CryptOMaMa program with various command line options.
    """
    parser = argparse.ArgumentParser(
                    prog='CryptOMaMa',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    
    parser.add_argument('mode',choices=['run', 'test'], \
                        help='Specify if you want "run" or "test" a strategy.')
    parser.add_argument('--input_file', help='Specify input files')
    parser.add_argument('--api', type=str, help='API (ex: binance)')
    parser.add_argument('--api_key', type=str, help='API key')
    parser.add_argument('--private_key', type=str, help='Path to your private key')
    parser.add_argument('--symbol', type=str, help='Symbol (ex: BTCUSDT)')
    parser.add_argument('--model', type=str, help='Modèle (ex: GueantLehalleFernandezTapia)')
    
    return parser

def process_inputs_from_json(args):
    """
    Process input data from a JSON file, updating argument values accordingly.
    """
    try:
        with open(args.input_file, 'r') as file:
            json_data = json.load(file)

            # Update the value of the "use_api" key if it is present in the JSON data
            if 'use_api' in json_data:
                # Update the values of the existing_args object with those from the
                # "use_api" section
                api_data = json_data['use_api']
                for key, value in api_data.items():
                    setattr(args, key, value)

            # Update the value of the "model" key if it is present in the JSON data
            if 'model' in json_data:
                setattr(args, 'model', json_data['model'])

        return args

    except FileNotFoundError:
        print(f'The file {args.input_file} does not exist.')
    except json.JSONDecodeError:
        print(f'JSON decoding error in the file {args.input_file}.\
              Ensure it is in valid JSON format.')
