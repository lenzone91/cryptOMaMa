# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import unittest
from src.model_tools.model import Model

class TestModel(unittest.TestCase):
    """
    Model class test
    """

    def test_compute_quotes_not_implemented(self):
        """
        Testing of compute quotes TypeError
        """
        # Create an anonymous subclass of Model without implementing compute_quotes
        class MockModel(Model):
            '''
            Initialize empty class for tests
            '''
            pass

        # Use the assertRaises context to check if NotImplementedError is raised
        with self.assertRaises(TypeError) as context:
            MockModel()

        # Ensure that the error message is as expected
        expected_error_message = "Can't instantiate abstract class MockModel with "+\
            "abstract method __init__"
        self.assertEqual(str(context.exception), expected_error_message)

if __name__ == '__main__':
    unittest.main()
