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
if sys.platform in ["darwin", "linux"]:
    fontdir = "../fonts/"

    TEXT = sys.argv[-1]
    if TEXT and TEXT.endswith(".py"):
        TEXT = "42"
else:
    fontdir = ""
    TEXT = "42"

from gui import testrunner
from gui.ui.monoc import Mlabel
import lvgl as lv


async def test(scr, display=None):
    scr.set_style_bg_opa(lv.OPA.COVER, 0)
    # display.lv_display.set_antialiasing(False)
    text = TEXT
    l_sz14 = Mlabel(scr, text=text, scr=False)
    l_sz14.align(lv.ALIGN.CENTER, 0, 0)

    print("MONO FONT TEST:")

    for _font in [f for f in sorted(os.listdir(fontdir)) if f.endswith(".bin")]:
        # print(f"- {_font}")
        with open(f"{fontdir}{_font}", "rb") as fb:
            font_data = fb.read()
        font = lv.binfont_create_from_buffer(font_data, len(font_data))

        l_sz14.set_style_text_font(font, 0)

        l_sz14.align(lv.ALIGN.CENTER, 0, 0)

        # await asyncio.sleep_ms(500)  # await so the frame can be rendered
        i = 0
        while True:
            i += 1
            await asyncio.sleep_ms(5)
            if i == 100:
                break

    print("OK")


__file__ = globals().get("__file__", "test")

try:
    import display_config

except Exception:
    display_config = testrunner.display_config


display_config.MODE = "interactive"
display_config.INDEV = "sim"
testrunner.run(test, __file__, disp_config=display_config)
