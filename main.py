"""
OMaMa Version 0.0.1
"""

import traceback
from src.utils.args_reading import process_arguments
from src.launcher import Launcher


if __name__ == "__main__":

    args = process_arguments()

    try:
        launcher = Launcher(args)
        launcher.launch()

    except Exception as e:
        print("Terminated unsuccessfully")
        traceback.print_exc()
        raise Exception("Terminated unsuccessfully") from e
        