import sys
import asyncio
import os
import pyb
import lvgl as lv

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner

from monoc import Mbutton

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


async def demo(scr, display=None):
    mbar = Mbutton(scr, scr=False)

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO BUTTON TEST:")
    i = 0
    while True:
        if pyb.Switch().value():
            i += 1
            # mbar.set_mvalue(i)
            mbar.send_event(lv.EVENT.PRESSED, None)
            print(i)

        else:
            mbar.send_event(lv.EVENT.RELEASED, None)
        await asyncio.sleep_ms(200)
        if i == 3:
            mbar.send_event(lv.EVENT.RELEASED, None)

            await asyncio.sleep_ms(200)
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
