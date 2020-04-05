from time import sleep

import sys
from pathlib import Path
import sys, os


import os
two_up = os.path.dirname(os.getcwd())
print(two_up)
#
# exit(0)
# print(Path(__file__))
# print(Path(__file__).parents[0])
# print(Path(__file__).parents[1])
# exit(0)

# parentPath = Path(__file__).parents[1]
addPath = os.path.join(os.path.dirname(two_up), 'pySX127x')
print('add path:', addPath)
sys.path.append(addPath)
from pySX127x.LoRa import *
from pySX127x.board_config import BOARD
BOARD.setup()