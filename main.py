# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"
__version__ = "0.1.0"
__maintainer__ = "Enzo COGNEVILLE"
__email__ = "cognenzo@gmail.com"
__status__ = "Proof of concept"

import traceback
from src.utils.args_reading import process_arguments
from src.launcher import Launcher

if __name__ == "__main__":

    args = process_arguments()

    #try:
    launcher = Launcher(args)
    launcher.launch()

    """except Exception as e:
        print("Terminated unsuccessfully")
        traceback.print_exc()
        raise Exception("Terminated unsuccessfully") from e"""
        