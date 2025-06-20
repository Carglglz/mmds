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
from gui.ui.monoc import StatusBar
from gui.mgui import Clock
import lvgl as lv
import time

# This is a status bar test


async def status_bar(scr, display=None):
    sbar = StatusBar(scr, scr=False)
    clk = Clock()

    print("MONO STATUS BAR TEST:")
    i = 0

    sbar.wifi.set_wvalue(i - 100)
    sbar.batt.set_bvalue(i)

    t0 = time.mktime(time.localtime())
    dt = time.mktime(time.localtime()) - t0
    sbar.clock.set_text(f"{clk.tmdelta_fmt(dt)[3:]}")
    # display.debug_display(True)  # enable frame debug
    await display.screenshot(name="start", debug=False)  # screenshot + frame debug
    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    t0 = time.mktime(time.localtime())
    while True:
        sbar.batt.set_bvalue(i)
        sbar.wifi.set_wvalue(i - 100)

        dt = time.mktime(time.localtime()) - t0
        sbar.clock.set_text(f"{clk.tmdelta_fmt(dt)[3:]}")
        await asyncio.sleep_ms(20)

        print(i)
        if i == 100:
            print("OK")
            break
        i += 1

    await display.screenshot(name="end", debug=False)  # screenshot + frame debug
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
testrunner.run(status_bar, __file__, disp_config=display_config)
testrunner.devicereset()
