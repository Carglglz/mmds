import sys
import asyncio

try:
    # running from sim/device
    import os

    sys.path.append(os.getcwd())
    import board_config

except ImportError:
    # running from micropython test suite
    root_testdir = sys.path[0].rsplit("/", 2)[0]
    sys.path.append(f"{root_testdir}")
    sys.path.append(f"{root_testdir}/displays/sim")

# print(sys.path)

from gui import testrunner
from gui.ui.monoc import Marc

# This is a basic arc test


async def test(scr, display=None):
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

except Exception:
    display_config = testrunner.display_config


display_config.MODE = "interactive"
display_config.POINTER = "sim"
testrunner.run(test, __file__, disp_config=display_config)
testrunner.devicereset()
