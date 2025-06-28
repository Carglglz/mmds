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
import lvgl as lv

# This is a basic bar test


async def test(scr, display=None):
    if hasattr(lv, "qrcode"):
        text = "https://lvgl.io/"
        _qr = lv.qrcode(scr)
        _qr.set_size(60)
        _qr.center()
        _qr.set_style_border_color(lv.color_white(), 0)
        _qr.set_style_border_width(2, 0)
        _qr.update(text, len(text))

    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO QR TEST:")
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
display_config.INDEV = "sim"
testrunner.run(test, __file__, disp_config=display_config)
testrunner.devicereset()
