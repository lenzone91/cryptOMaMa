###############################
# input arguments treatment   #
###############################

import optparse
import json

def process_arguments():
    PARSER = create_parser()
    (OPTIONS, ARGS) = PARSER.parse_args()

    args = None

    if OPTIONS.input_file:
        args = process_inputs_from_json(OPTIONS.input_file)
    return args

def create_parser():
    PARSER = optparse.OptionParser()
    PARSER.add_option('--input_file', dest='input_file', help='Specify input files')
    return PARSER

def process_inputs_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        print(f'The file {json_file} does not exist.')
    except json.JSONDecodeError:
        print(f'JSON decoding error in the file {json_file}. Ensure it is in valid JSON format.')
