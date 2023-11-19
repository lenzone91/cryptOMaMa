from src.api_tools.brokers.binance import Binance

def create_broker(api, api_key, private_key):
    if api == "binance":
        return Binance(api_key, private_key)
    #elif api == "cryptocom":
    #    return CryptoCom(api_key, private_key)
    # Ajoutez d'autres cas selon les besoins pour de nouveaux brokers
    else:
        raise ValueError(f"Unsupported broker type: {api}")