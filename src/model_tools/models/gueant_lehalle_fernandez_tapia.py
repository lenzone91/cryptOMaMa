# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import numpy as np
from ..model import Model

class GueantLehalleFernandezTapia(Model):
    """
    Implementation of the Gueant Lehalle Fernandez Tapia model.

    Notes
    -----
    More detail on the implemented model at : 
    https://arxiv.org/abs/1105.3115
    Dealing with the Inventory Risk. A solution to the market making problem.
    Olivier Guéant, Charles-Albert Lehalle, Joaquin Fernandez Tapia

    Parameters
    ----------
    None

    Methods
    -------
    compute_quotes()
    """

    def __init__(self):
        super().__init__("GueantLehalleFernandezTapia")

    def compute_quotes(self, with_penalty: bool, A: float, k: float,
                       q: float, delta: float, gamma: float, sigma: float, xi: float) -> (float,float):
        """
        Implement the quote computations method in one dimension.

        Parameters
        ----------
        with_penalty : bool
            Define if there is a penalty value
        A : float
            The second parameter.
        k : float
            The second parameter.
        q : float
            The second parameter.
        delta : float
            The second parameter.
        gamma : float
            The second parameter.
        sigma : float
            The second parameter.
        xi : float
            The second parameter.        
            
        Returns
        -------
        bid_quote : float
            The best bid quote value
        ask_quote : float
            The best ask quote value
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
