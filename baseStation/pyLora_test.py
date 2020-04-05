from time import sleep

import sys
from pathlib import Path
import sys, os

# print(Path(__file__).parents[0])
# print(Path(__file__).parents[1])
# print(Path(__file__))

parentPath = Path(__file__).parents[1]
addPath = os.path.join(os.path.dirname(parentPath), 'pySX127x')
sys.path.append(addPath)
from pySX127x.LoRa import *
from pySX127x.board_config import BOARD
BOARD.setup()