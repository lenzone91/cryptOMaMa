#OMaMa Version 0.0.1

import optparse
import traceback
from src.models.gueant_lehalle_fernandez_tapia import GueantLehalleFernandezTapia

if __name__ == "__main__":

    PARSER = optparse.OptionParser()
    (OPTIONS, ARGS) = PARSER.parse_args()
    print(ARGS)
    try:
        glft = GueantLehalleFernandezTapia()

        bid, ask = glft.compute_quotes(True,1,1,10,1,1,1,0)

        print(bid, ask)

    except Exception as e:
        print("Terminated unsuccessfully")
        traceback.print_exc()
        raise Exception("Terminated unsuccessfully")
        