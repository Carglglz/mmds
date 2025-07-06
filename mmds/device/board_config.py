import sys
import os
import random
import machine

machine.freq(240000000)


# sys.path is = ['', '.frozen'] by default so
# To run from frozen: # uncomment
sys.path[0], sys.path[1] = sys.path[1], sys.path[0]

sys.path.append(f"{os.getcwd()}/display")

sys.path.append("/audio")

from espbuzz import AsyncBuzzer

from battery import battery


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


class ADC:
    def __init__(self, rng=(2000, 3000)):
        self.rng = rng

    def read(self):
        return random.randint(*self.rng)


adc = machine.ADC(machine.Pin(34))
adc.atten(machine.ADC.ATTN_11DB)
# adc.deinit()
# adc = ADC()
# stemp = ADC(rng=(800, 1000))
stemp = machine.ADC(machine.Pin(36))
stemp.atten(machine.ADC.ATTN_11DB)

dt = 100

bz = SoundDevice(AsyncBuzzer(25), fq=1440)
bz.beep()

conf = {"adc": adc, "temp": stemp, "dt": dt, "buzz": bz, "batt": battery}
