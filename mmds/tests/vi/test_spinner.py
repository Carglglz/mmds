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
import lvgl as lv

# from gui.ui.monoc import Marc

# This is a basic arc test


async def test(scr, display=None):
    spinner = lv.spinner(scr)
    spinner.set_size(50, 50)
    spinner.center()
    spinner.set_style_bg_color(lv.color_black(), 0)
    spinner.set_style_arc_color(lv.color_black(), 0)
    spinner.set_style_arc_color(lv.color_white(), lv.PART.INDICATOR)
    spinner.set_style_arc_width(5, lv.PART.INDICATOR)

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO SPINNER TEST:")
    i = 0
    while True:
        i += 1
        print(i)
        await asyncio.sleep_ms(5)
        if i == 250:
            print("OK")
            break

    await asyncio.sleep_ms(5)


__file__ = globals().get("__file__", "test")

try:
    import display_config

except Exception:
    display_config = testrunner.display_config


display_config.MODE = "interactive"
display_config.INDEV = "sim"
testrunner.run(test, __file__, disp_config=display_config)
testrunner.devicereset()
