# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

from abc import ABC, abstractmethod

class Model(ABC):
    """
    Abstract base class for models
    """
    @abstractmethod
    def compute_quotes(self):
        """
        Abstract method for compute quotes.
        """
