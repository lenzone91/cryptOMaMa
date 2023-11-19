import unittest
from src.model_tools.model import Model

class TestModel(unittest.TestCase):

    def test_compute_quotes_not_implemented(self):
        # Create an anonymous subclass of Model without implementing compute_quotes
        class MockModel(Model):
            pass

        # Use the assertRaises context to check if NotImplementedError is raised
        with self.assertRaises(TypeError) as context:
            MockModel()

        # Ensure that the error message is as expected
        expected_error_message = "Can't instantiate abstract class MockModel with abstract method compute_quotes"
        self.assertEqual(str(context.exception), expected_error_message)

if __name__ == '__main__':
    unittest.main()