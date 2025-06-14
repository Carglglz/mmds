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
from gui.ui.monoc import Mlabel
import lvgl as lv


async def test(scr, display=None):
    scr.set_style_bg_opa(lv.OPA.COVER, 0)
    # display.lv_display.set_antialiasing(False)
    text = "12345\nabcdfg"
    l_sz14 = Mlabel(scr, text=text, scr=False)

    l_sz14.set_style_text_font(lv.font_montserrat_14, 0)
    l_sz14.align(lv.ALIGN.CENTER, 0, 0)
    l_sz14.set_style_text_opa(lv.OPA.COVER, 0)
    l_sz14.set_style_text_outline_stroke_opa(lv.OPA.COVER, 0)
    l_sz24 = Mlabel(scr, text=text, scr=False)
    l_sz24.align(lv.ALIGN.CENTER, 0, 0)
    l_sz24.add_flag(lv.obj.FLAG.HIDDEN)

    # await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO LABEL TEST:")
    i = 0
    while True:
        i += 1
        await asyncio.sleep_ms(20)
        if i == 100:
            break

    l_sz14.add_flag(lv.obj.FLAG.HIDDEN)

    l_sz24.remove_flag(lv.obj.FLAG.HIDDEN)

    i = 0
    while True:
        i += 1
        await asyncio.sleep_ms(20)
        if i == 100:
            break

    scr.set_style_bg_color(lv.color_white(), 0)

    l_sz14.set_style_text_color(lv.color_black(), 0)
    l_sz24.set_style_text_color(lv.color_black(), 0)

    l_sz14.remove_flag(lv.obj.FLAG.HIDDEN)
    l_sz24.add_flag(lv.obj.FLAG.HIDDEN)

    i = 0
    while True:
        i += 1
        await asyncio.sleep_ms(20)
        if i == 100:
            break

    l_sz14.add_flag(lv.obj.FLAG.HIDDEN)

    l_sz24.remove_flag(lv.obj.FLAG.HIDDEN)

    i = 0
    while True:
        i += 1
        await asyncio.sleep_ms(20)
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
