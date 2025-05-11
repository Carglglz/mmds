import sys
import asyncio


import testrunner

from ui.monoc import StatusBar, Thermometer, MMenu, MChart, Mlabel  # noqa
import aiorepl
import time
import lvgl as lv  # noqa


class Clock:
    def __init__(self): ...

    def _dt_format(self, number):
        n = str(int(number))
        if len(n) == 1:
            n = "0{}".format(n)
            return n
        else:
            return n

    def time_str(self, uptime_tuple):
        upt = [self._dt_format(i) for i in uptime_tuple[:]]
        up_str_2 = f"{upt[0]}:{upt[1]}:{upt[2]}"
        return up_str_2

    def tmdelta_fmt(self, dt):
        hh, mm, ss = (0, 0, 0)
        mm = dt // 60
        ss = dt % 60
        if mm:
            pass
        else:
            return self.time_str((hh, mm, ss))
        hh = mm // 60
        if hh:
            mm = mm % 60
        else:
            return self.time_str((hh, mm, ss))
        return self.time_str((hh, mm, ss))

    def time(self):
        if sys.platform in ["darwin", "linux"]:
            return f"{self.time_str(time.localtime()[-6:-3])[:-3]}"
        else:
            return f"{self.time_str(time.localtime()[-5:-2])[:-3]}"


class TMP36:
    def __init__(self, adc=None):
        self.adc = adc

    def read_tmp(self):
        return (((self.adc.read() / 4095) * 3.3) - 0.5) * 100


async def gui(scr, display=None, adc=None, temp=None, dt=20):
    # TEMP SENSOR
    ts = TMP36(temp)

    # STATUS BAR
    sb = StatusBar(scr, scr=False)

    # CLOCK
    clk = Clock()

    # APPS
    # THERMOMETER
    thm = Thermometer(scr, rng=(0, 50), scr=False)
    thm.align(lv.ALIGN.LEFT_MID, 0, 0)
    thm_lab = lv.label(scr)
    thm_lab.set_style_text_color(lv.color_white(), 0)
    thm_lab.set_style_text_font(lv.font_montserrat_24, 0)
    thm_lab.align(lv.ALIGN.CENTER, 10, 0)
    thm.add_flag(lv.obj.FLAG.HIDDEN)
    thm_lab.add_flag(lv.obj.FLAG.HIDDEN)

    # PLOT
    plot = MChart(scr, y_range=(200, 300), scr=False)
    plot.set_data_func(ts.read_tmp)
    plot.add_flag(lv.obj.FLAG.HIDDEN)
    plot.graph.add_flag(lv.obj.FLAG.HIDDEN)
    plot.lab.add_flag(lv.obj.FLAG.HIDDEN)

    # INFO
    info = Mlabel(scr, text="Hello", scr=False)
    _mpv = "MPY v{}.{}".format(*sys.implementation.version[:-2])
    _lvglv = f"LVGL v{lv.version_major()}.{lv.version_minor()}"
    info.set_text(f"{_mpv}\n{_lvglv}")
    info.set_width(125)
    info.set_long_mode(lv.label.LONG_MODE.WRAP)
    info.align(lv.ALIGN.LEFT_MID, 0, 0)
    info.set_style_text_font(lv.font_montserrat_14, 0)
    info.add_flag(lv.obj.FLAG.HIDDEN)

    # MENU
    menu = MMenu(scr, scr=False)
    menu.apps[menu.btn1] = [thm, thm_lab]
    menu.apps[menu.btn2] = [plot, plot.lab, plot.graph]
    menu.apps[menu.btn3] = [info]

    wgroup = lv.group_create()
    wgroup.add_obj(menu.btn1)
    wgroup.add_obj(menu.btn2)
    wgroup.add_obj(menu.btn3)
    display.indev_test.set_group(wgroup)

    # AIOREPL
    g = __import__("__main__").__dict__
    g.update(dummy=display, clock=clk, ts=ts, thm=thm)
    aiorepl_task = asyncio.create_task(aiorepl.task(g))

    print("OK")
    try:
        while True:
            i = int((adc.read() / 4095) * 100)
            tmp = ts.read_tmp()
            sb.batt.set_bvalue(100 - i)
            sb.wifi.set_wvalue(-i)
            sb.clock.set_text(clk.time())

            thm.set_tvalue(int(tmp))
            thm_lab.set_text(f"{tmp:.1f} C")

            plot.update(scale=10)

            await asyncio.sleep_ms(dt)

    except KeyboardInterrupt:
        print("DONE")


__file__ = globals().get("__file__", "gui")

try:
    import display_config

except Exception:
    display_config = testrunner.display_config


def run(**kwargs):
    testrunner.run(gui, __file__, disp_config=display_config, **kwargs)
    testrunner.devicereset()
