import sys
import os

sys.path.append(f"{os.getcwd()}/app")
sys.path.append(f"{os.getcwd()}/display")

import pyb

adc = pyb.ADC(pyb.Pin.board.X19)
stemp = pyb.ADC(pyb.Pin.board.Y11)
dt = 20

conf = {"adc": adc, "temp": stemp, "dt": dt}
