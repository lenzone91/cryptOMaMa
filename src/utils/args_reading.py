# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import argparse
import json

def process_arguments():
    """
    Process command line arguments, including optional input file processing.
    """

    parser = create_parser()
    args = parser.parse_args()
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

    parser.add_argument('CMD',choices=['run', 'test'], \
                        help='Specify if you want "run" or "test" a strategy.')
    parser.add_argument('--input_file', help='Path to a JSON input file')

    return parser

def process_inputs_from_json(args):
    """
    Process input data from a JSON file, updating argument values accordingly.
    """
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            
            json_data = json.load(file)

            for key, value in json_data.items():
                    setattr(args, key, value)

        return args

    except FileNotFoundError as exc:
        raise ValueError(f'The file {args.input_file} does not exist.') from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f'JSON decoding error in the file {args.input_file}.\
              Ensure it is in valid JSON format.') from exc
