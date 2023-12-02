# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

from .models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia

def create_model(model):
    """
    Factory method to create the correct instance of a model
    """

    if model == "GueantLehalleFernandezTapia":
        return GueantLehalleFernandezTapia()
    # Ajoutez d'autres cas selon les besoins pour de nouveaux brokers
    raise ValueError(f"Unsupported model type: {model}")
