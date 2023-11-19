"""
Useful methods for managing all models like a factory method
"""

from src.model_tools.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia

def create_model(model):
    """
    Factory method to create the correct instance of a model
    """

    if model == "GueantLehalleFernandezTapia":
        return GueantLehalleFernandezTapia()
    # Ajoutez d'autres cas selon les besoins pour de nouveaux brokers
    raise ValueError(f"Unsupported model type: {model}")
