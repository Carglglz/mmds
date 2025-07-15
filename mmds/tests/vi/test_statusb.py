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
import time
from gui.mgui import Clock

# This is a status bar test


async def test(scr, display=None):
    sbar = StatusBar(scr, scr=False)
    clk = Clock()

    print("MONO STATUS BAR TEST:")
    i = 0

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


__file__ = globals().get("__file__", "test")

try:
    import display_config

    display_config.MODE = "interactive"
    display_config.INDEV = "sim"
except Exception:
    display_config = testrunner.display_config


testrunner.run(test, __file__, disp_config=display_config)
