import sys
import asyncio
import lvgl as lv

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

from gui import testrunner
from gui.ui.monoc import Mbutton

# This is a basic button test


async def test(scr, display=None):
    mbtn = Mbutton(scr, scr=False, pc=True, focus=True)

    wgroup = lv.group_create()
    wgroup.add_obj(mbtn)
    display.indev.set_group(wgroup)

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO BUTTON TEST:")
    while True:
        await asyncio.sleep_ms(200)
        if mbtn._np >= 3:
            await asyncio.sleep_ms(200)
            print("OK")
            break


__file__ = globals().get("__file__", "test")

try:
    import display_config

except Exception:
    display_config = testrunner.display_config


display_config.MODE = "interactive"
display_config.POINTER = "encoder"
testrunner.run(test, __file__, disp_config=display_config)
testrunner.devicereset()
