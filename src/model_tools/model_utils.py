from src.model_tools.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia

def create_model(model):
    if model == "GueantLehalleFernandezTapia":
        return GueantLehalleFernandezTapia()
    # Ajoutez d'autres cas selon les besoins pour de nouveaux brokers
    else:
        raise ValueError(f"Unsupported model type: {model}")