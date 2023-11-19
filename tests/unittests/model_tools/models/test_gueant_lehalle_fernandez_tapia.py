import unittest
from src.model_tools.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia

class TestGueantLehalleFernandezTapia(unittest.TestCase):

    def test_compute_quotes_with_penalty(self):
        model = GueantLehalleFernandezTapia()
        with_penalty = True
        A, k, q, delta, gamma, sigma, xi = 1, 1, 10, 1, 1, 1, 0
        bid_quote, ask_quote = model.compute_quotes(with_penalty, A, k, q, delta, gamma, sigma, xi)

        # Add assertions based on the expected results
        self.assertEqual(bid_quote, 13.241130903384901)
        self.assertEqual(ask_quote, -10.07530891258634)

    def test_compute_quotes_without_penalty(self):
        model = GueantLehalleFernandezTapia()
        with_penalty = False
        A, k, q, delta, gamma, sigma, xi = 1, 2, 3, 4, 5, 6, 7
        bid_quote, ask_quote = model.compute_quotes(with_penalty, A, k, q, delta, gamma, sigma, xi)

        # Add assertions based on the expected results
        self.assertEqual(bid_quote, 0)
        self.assertEqual(ask_quote, 0)

if __name__ == '__main__':
    unittest.main()
