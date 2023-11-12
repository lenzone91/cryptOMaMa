from src.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia
from src.scrap_data.binance import Binance
class Launcher(object):

    def __init__(self, args):
        self.actions=args["actions"]

    def launch(self):
        for action in self.actions : 
            if "compute_quotes" in action :
                self.create_model(action["compute_quotes"])
                print(self.model.compute_quotes(True,1,1,10,1,1,1,0))
            elif "use_api" in action :
                if action["use_api"]["api"] == "binance":
                    api_key = action["use_api"]["api_key"]
                    private_key = action["use_api"]["private_key"]
                    symbol = action["use_api"]["symbol"]

                    self.binance = Binance(api_key,private_key)
                    bids, asks = self.binance.get_depth(symbol)
                    print(bids)

    def create_model(self, action):
        if action["model"] == "GueantLehalleFernandezTapia":
            self.model = GueantLehalleFernandezTapia()

        
    
    