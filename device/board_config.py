import sys
import os

sys.path.append(f"{os.getcwd()}/gui")
sys.path.append(f"{os.getcwd()}/display")
sys.path.append(f"{os.getcwd()}/audio")

import pyb
from pybbuzz import Buzzer


class SoundDevice:
    def __init__(self, buzz, mute=False):
        self.sd = buzz
        self._mute = mute

    def beep(self, sleeptime=50, ntimes=1, ntimespaced=50, fq=2500):
        if not self._mute:
            self.sd.buzz_beep(sleeptime, ntimes, ntimespaced, fq)

    def mute(self, b=None):
        if b is None:
            self._mute = not self._mute
        else:
            self._mute = b


adc = pyb.ADC(pyb.Pin.board.X19)
stemp = pyb.ADC(pyb.Pin.board.Y11)
dt = 20
bz = SoundDevice(Buzzer("X1"))
bz.beep()


conf = {"adc": adc, "temp": stemp, "dt": dt, "buzz": bz}
