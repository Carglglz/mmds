import sys
import asyncio
import os
import pyb

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner
from monoc import Mbar
import aiorepl
import lvgl as lv  # noqa

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


async def demo(scr, display=None):
    dummy = Mbar(scr, w=lv.pct(60), scr=False)
    adc = pyb.ADC(pyb.Pin.board.X19)

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MBAR - ADC TEST:")
    g = __import__("__main__").__dict__
    g.update(dummy=dummy)
    aiorepl_task = asyncio.create_task(aiorepl.task(g))

    print("OK")
    i = 0
    try:
        while True:
            # bar/arc + potentiometer
            i = int((adc.read() / 4095) * 100)
            # mbar.set_mvalue(i)
            await asyncio.sleep_ms(20)
            dummy.set_mvalue(i)
            if i == 100:
                print("DONE")
                break

    except KeyboardInterrupt:
        print("DONE")
        # lv.deinit()


__file__ = globals().get("__file__", "test")

try:
    import display_config

    display_config.MODE = "interactive"
    display_config.POINTER = "sim"
except Exception:
    display_config = testrunner.display_config


testrunner.run(demo, __file__, disp_config=display_config)
testrunner.devicereset()
