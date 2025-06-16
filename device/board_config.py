import sys
import os

# sys.path is = ['', '.frozen'] by default so
# To run from frozen: # uncomment

sys.path[0], sys.path[1] = sys.path[1], sys.path[0]

sys.path.append(f"{os.getcwd()}/display")
sys.path.append(f"{os.getcwd()}/audio")

import pyb
from pybbuzz import Buzzer


class SoundDevice:
    def __init__(self, buzz, mute=False, fq=2500):
        self.sd = buzz
        self._mute = mute
        self.fq = fq

    def beep(self, sleeptime=50, ntimes=1, ntimespaced=50):
        if not self._mute:
            fq = self.fq
            self.sd.buzz_beep(sleeptime, ntimes, ntimespaced, fq)

    def mute(self, b=None):
        if b is None:
            self._mute = not self._mute
        else:
            self._mute = b


adc = pyb.ADC(pyb.Pin.board.X19)
stemp = pyb.ADC(pyb.Pin.board.Y11)
dt = 100
bz = SoundDevice(Buzzer("X1"))
bz.beep()


conf = {"adc": adc, "temp": stemp, "dt": dt, "buzz": bz}
