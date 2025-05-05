import sys
import asyncio
import os

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner

sys.path.append(sys.path[0].rsplit("/", 1)[0])
from monoc import Marc

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


async def demo(scr, display=None):
    mbar = Marc(scr, scr=False)

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO ARC TEST:")
    i = 0
    while True:
        i += 1
        mbar.set_mvalue(i)
        print(i)
        await asyncio.sleep_ms(5)
        if i == 100:
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
