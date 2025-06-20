import sys
import asyncio
import os

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner

sys.path.append(sys.path[0].rsplit("/", 1)[0])
from monoc import Marc

import pyb

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


async def demo(scr, display=None):
    mbar = Marc(scr, scr=False)

    adc = pyb.ADC(pyb.Pin.board.X19)
    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO ARC-ADC TEST:")
    i = 0
    while True:
        # bar/arc + potentiometer
        i = int((adc.read() / 4095) * 100)
        mbar.set_mvalue(i)
        await asyncio.sleep_ms(20)
        if i == 100:
            print(i)
            print("OK")
            break


__file__ = globals().get("__file__", "test")

try:
    import display_config

    display_config.MODE = "interactive"
    display_config.POINTER = "sim"
except Exception:
    display_config = testrunner.display_config


testrunner.run(demo, __file__, disp_config=display_config)
testrunner.devicereset()
