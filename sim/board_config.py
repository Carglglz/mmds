import sys
import os
import random


sys.path.append(f"{os.getcwd()}/app")
sys.path.append(f"{os.getcwd()}/display")


class ADC:
    def __init__(self, rng=(2000, 3000)):
        self.rng = rng

    def read(self):
        return random.randint(*self.rng)


adc = ADC()
stemp = ADC(rng=(800, 1000))
dt = 500

conf = {"adc": adc, "temp": stemp, "dt": dt}
