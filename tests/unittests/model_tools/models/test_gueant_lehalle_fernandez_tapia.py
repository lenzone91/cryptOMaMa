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

class TestGueantLehalleFernandezTapia(unittest.TestCase):
    """
    GueantLehalleFernandezTapia class test
    """

    def test_compute_quotes_with_penalty(self):
        """
        Testing of compute quotes with penalty in one dimension
        """
        model = GueantLehalleFernandezTapia()
        with_penalty = True
        a, k, q, delta, gamma, sigma, xi = 1, 1, 10, 1, 1, 1, 0
        bid_quote, ask_quote = model.compute_quotes(with_penalty, a, k, q, delta, gamma, sigma, xi)

        # Add assertions based on the expected results
        self.assertEqual(bid_quote, 13.241130903384901)
        self.assertEqual(ask_quote, -10.07530891258634)

    def test_compute_quotes_without_penalty(self):
        """
        Testing of compute quotes without penalty in one dimension
        """
        model = GueantLehalleFernandezTapia()
        with_penalty = False
        a, k, q, delta, gamma, sigma, xi = 1, 2, 3, 4, 5, 6, 7
        bid_quote, ask_quote = model.compute_quotes(with_penalty, a, k, q, delta, gamma, sigma, xi)

        # Add assertions based on the expected results
        self.assertEqual(bid_quote, 0)
        self.assertEqual(ask_quote, 0)

if __name__ == '__main__':
    unittest.main()
