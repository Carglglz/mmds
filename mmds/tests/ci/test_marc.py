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

from gui import testrunner
from gui.ui.monoc import Marc
import lvgl as lv

# This is a basic arc test


async def mono_arc_test(scr, display=None):
    marc = Marc(scr, scr=False)
    marc.set_mvalue(0)

    display.debug_display(True)  # enable frame debug
    await display.screenshot(name="start", debug=True)  # screenshot + frame debug
    await asyncio.sleep_ms(500)  # await so the frame can be rendered

    print("MONO ARC TEST:")
    display.debug_display(False)
    i = 0
    while True:
        i += 1
        marc.set_mvalue(i)
        await asyncio.sleep_ms(5)
        if i == 100:
            print("OK")
            break

    display.debug_display(True)
    await display.screenshot(name="end", debug=True)
    await asyncio.sleep_ms(500)  # await so the frame can be rendered


__file__ = globals().get("__file__", "test")

try:
    import display_config

except Exception:
    display_config = testrunner.display_config


# OVERRIDE display_config
display_config.MODE = "sim"
display_config.POINTER = "sim"
display_config.COLOR_FORMAT = lv.COLOR_FORMAT.RGB888
display_config.WIDTH = 128
display_config.HEIGHT = 64
testrunner.run(mono_arc_test, __file__, disp_config=display_config)
testrunner.devicereset()
