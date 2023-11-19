import unittest
from src.model_tools.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia
from src.model_tools.model_utils import create_model

class TestModelUtils(unittest.TestCase):

    def test_create_model_gueant_lehalle_fernandez_tapia(self):
        model_type = "gueant_lehalle_fernandez_tapia"
        model_instance = create_model(model_type)

        # Ensure that the created model is an instance of GueantLehalleFernandezTapia
        self.assertIsInstance(model_instance, GueantLehalleFernandezTapia)

    def test_create_model_unsupported_model_type(self):
        unsupported_model_type = "unsupported_model"
        
        # Use the assertRaises context to check if ValueError is raised
        with self.assertRaises(ValueError) as context:
            create_model(unsupported_model_type)

        # Ensure that the error message is as expected
        expected_error_message = f"Unsupported model type: {unsupported_model_type}"
        self.assertEqual(str(context.exception), expected_error_message)

if __name__ == '__main__':
    unittest.main()
