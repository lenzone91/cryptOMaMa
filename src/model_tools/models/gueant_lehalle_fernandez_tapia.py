# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import numpy as np
from src.model_tools.model import Model

class GueantLehalleFernandezTapia(Model):
    """
    Implementation of the Gueant Lehalle Fernandez Tapia model.
    """

    def __init__(self):
        super().__init__()

    def compute_quotes(self, with_penalty, A, k, q, delta, gamma, sigma, xi):
        """
        Implement the quote computations method in one dimension.
        """
        if with_penalty:
            if xi == 0:
                bid_quote = (1/k)+((2*q+delta)/2)*\
                    np.sqrt((gamma*np.power(sigma,2)*np.exp(1))/(2*A*delta*k))
                ask_quote = (1/k)-((2*q-delta)/2)*\
                    np.sqrt((gamma*np.power(sigma,2)*np.exp(1))/(2*A*delta*k))
        else :
            bid_quote = 0
            ask_quote = 0
        return bid_quote, ask_quote
