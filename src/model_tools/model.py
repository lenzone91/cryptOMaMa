"""
Abstract base class for models
"""

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
