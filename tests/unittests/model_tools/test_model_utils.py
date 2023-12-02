# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import unittest
from src.model_tools.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia
from src.model_tools.model_utils import create_model

class TestModelUtils(unittest.TestCase):
    """
    Model utils methods test
    """

    def test_create_model_gueant_lehalle_fernandez_tapia(self):
        """
        Testing the creation of GueantLehalleFernandezTapia object
        """
        model_type = "GueantLehalleFernandezTapia"
        model_instance = create_model(model_type)

        # Ensure that the created model is an instance of GueantLehalleFernandezTapia
        self.assertIsInstance(model_instance, GueantLehalleFernandezTapia)

    def test_create_model_unsupported_model_type(self):
        """
        Testing the creation of GueantLehalleFernandezTapia object ValueError
        """
        unsupported_model_type = "unsupported_model"

        # Use the assertRaises context to check if ValueError is raised
        with self.assertRaises(ValueError) as context:
            create_model(unsupported_model_type)

        # Ensure that the error message is as expected
        expected_error_message = f"Unsupported model type: {unsupported_model_type}"
        self.assertEqual(str(context.exception), expected_error_message)

if __name__ == '__main__':
    unittest.main()
