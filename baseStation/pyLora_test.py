from time import sleep

import sys
import sys, os
print(os.path.dirname(sys.path[0]))
print(os.path.dirname(sys.path[1]))
print(os.path.dirname(sys.path[2]))


exit(0)
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'pySX127x'))
# from mymodule import MyModule
# sys.path.append("./../../pySX127x/")
from pySX127x.LoRa import *
from pySX127x.board_config import BOARD
BOARD.setup()