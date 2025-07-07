import sys
import os
import random


# sys.path is = ['', '.frozen'] by default so
# To run from frozen: # uncomment
# sys.path[0], sys.path[1] = sys.path[1], sys.path[0]

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
app = "demo"
