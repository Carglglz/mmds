import sys
import asyncio
import os

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner

sys.path.append(sys.path[0].rsplit("/", 1)[0])
from monoc import Mbar
import lvgl as lv

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


async def demo(scr, display=None):
    mbar = Mbar(scr, w=lv.pct(60), scr=False)

    wgroup = lv.group_create()
    wgroup.add_obj(mbar)
    display.indev_test.set_group(wgroup)
    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("MONO BAR-ENCODER TEST:")
    i = 0
    while True:
        i = mbar.get_value()
        # print(i)
        await asyncio.sleep_ms(5)
        if i == 100:
            print("OK")
            break


__file__ = globals().get("__file__", "test")

try:
    import display_config

    display_config.MODE = "interactive"
    display_config.INDEV = "encoder"
except Exception:
    display_config = testrunner.display_config


testrunner.run(demo, __file__, disp_config=display_config)
testrunner.devicereset()
