import sys
import asyncio
import os
import pyb
import math

sys.path.append("..")
sys.path.append(os.getcwd())
import testrunner

from monoc import StatusBar, Thermometer, MMenu, Marc, MChart, Mlabel  # noqa
import aiorepl
import time
import lvgl as lv  # noqa

# This is a basic test to test buttons, labels,
# RGB colors, layout aligment and events.


def _dt_format(number):
    n = str(int(number))
    if len(n) == 1:
        n = "0{}".format(n)
        return n
    else:
        return n


def time_str(uptime_tuple):
    upt = [_dt_format(i) for i in uptime_tuple[:]]
    up_str_2 = f"{upt[0]}:{upt[1]}:{upt[2]}"
    return up_str_2


def tmdelta_fmt(dt):
    hh, mm, ss = (0, 0, 0)
    mm = dt // 60
    ss = dt % 60
    if mm:
        pass
    else:
        return time_str((hh, mm, ss))
    hh = mm // 60
    if hh:
        mm = mm % 60
    else:
        return time_str((hh, mm, ss))
    return time_str((hh, mm, ss))


class IMU:
    def __init__(self):
        self.acc = pyb.Accel()

    def roll(self):
        """Return roll angle in degress"""
        ax, ay, az = self.acc.filtered_xyz()
        return math.atan2(ay, az) * (180 / math.pi)

    def pitch(self):
        """Return pitch angle in degress"""
        ax, ay, az = self.acc.filtered_xyz()
        return math.atan2(-ax, math.sqrt(ay * ay + az * az)) * (180 / math.pi)


class TMP36:
    def __init__(self, pin):
        self.adc = pyb.ADC(pin)

    def read_tmp(self):
        return (((self.adc.read() / 4095) * 3.3) - 0.5) * 100


async def demo(scr, display=None):
    # arc_imu = Marc(scr, w=44, h=44, rng=(0, 360), symb="o", scr=False)
    info = Mlabel(scr, text="Hello", scr=False)
    _mpv = "MPY v{}.{}".format(*sys.implementation.version[:-2])
    _lvglv = f"LVGL v{lv.version_major()}.{lv.version_minor()}"
    info.set_text(f"{_mpv}\n{_lvglv}")
    info.set_width(125)
    info.set_long_mode(lv.label.LONG_MODE.WRAP)
    info.align(lv.ALIGN.LEFT_MID, 0, 0)
    info.set_style_text_font(lv.font_montserrat_14, 0)
    dummy = StatusBar(scr, scr=False)
    adc = pyb.ADC(pyb.Pin.board.X19)
    imu = IMU()
    ts = TMP36(pyb.Pin.board.Y11)
    menu = MMenu(scr, scr=False)
    menu.select(0)
    thm = Thermometer(scr, rng=(0, 50), scr=False)
    plot = MChart(scr, y_range=(200, 300), scr=False)
    plot.set_data_func(ts.read_tmp)
    thm.align(lv.ALIGN.LEFT_MID, 0, 0)
    thm_lab = lv.label(scr)
    thm_lab.set_style_text_color(lv.color_white(), 0)
    thm_lab.set_style_text_font(lv.font_montserrat_24, 0)
    thm_lab.align(lv.ALIGN.CENTER, 10, 0)
    thm.add_flag(lv.obj.FLAG.HIDDEN)
    thm_lab.add_flag(lv.obj.FLAG.HIDDEN)
    # arc_imu.add_flag(lv.obj.FLAG.HIDDEN)
    # arc_imu.lab.add_flag(lv.obj.FLAG.HIDDEN)

    plot.add_flag(lv.obj.FLAG.HIDDEN)
    plot.graph.add_flag(lv.obj.FLAG.HIDDEN)
    plot.lab.add_flag(lv.obj.FLAG.HIDDEN)
    info.add_flag(lv.obj.FLAG.HIDDEN)
    menu.apps[menu.btn1] = [thm, thm_lab]
    menu.apps[menu.btn2] = [plot, plot.lab, plot.graph]
    # menu.apps[menu.btn3] = [arc_imu, arc_imu.lab]
    menu.apps[menu.btn3] = [info]
    await asyncio.sleep_ms(500)  # await so the frame can be rendered
    print("PRESS EVENT TEST:")
    g = __import__("__main__").__dict__
    g.update(dummy=display)
    aiorepl_task = asyncio.create_task(aiorepl.task(g))

    wgroup = lv.group_create()
    wgroup.add_obj(menu.btn1)
    wgroup.add_obj(menu.btn2)
    wgroup.add_obj(menu.btn3)
    display.indev_test.set_group(wgroup)

    print("OK")
    i = 0
    t0 = time.mktime(time.localtime())
    mode = 0
    try:
        while True:
            # bar/arc
            # if pyb.Switch().value():
            #     mode = not mode
            #     menu.press()
            #     i += 1
            #     if i > 100:
            #         i = 0
            #     mbar.set_mvalue(i)

            # bar/arc + potentiometer
            i = int((adc.read() / 4095) * 100)
            tmp = ts.read_tmp()
            # mbar.set_mvalue(i)
            await asyncio.sleep_ms(20)
            # if i <= 33:
            #     if menu.selected != 2:
            #         menu.select(2)

            # elif i >= 33 and i <= 66:
            #     if menu.selected != 1:
            #         menu.select(1)
            # else:
            #     if menu.selected != 0:
            #         menu.select(0)
            # if mode:
            #     dt = time.mktime(time.localtime()) - t0
            #     dummy.set_text(f"{tmdelta_fmt(dt)}")
            # else:
            #     dummy.set_text(f"{time_str(time.localtime()[-5:-2])}")
            dummy.batt.set_bvalue(100 - i)
            dummy.wifi.set_wvalue(-i)
            dummy.clock.set_text(f"{time_str(time.localtime()[-5:-2])[:-3]}")
            # if i == 100:
            # break

            thm.set_tvalue(int(tmp))
            thm_lab.set_text(f"{tmp:.1f} C")

            plot.update(scale=10)

            # accel + arc
            angle = int(imu.roll())
            # arc_imu.set_mvalue(angle)
            # await asyncio.sleep_ms(50)

    except KeyboardInterrupt:
        print("DONE")
        # lv.deinit()


__file__ = globals().get("__file__", "test")

try:
    import display_config

    display_config.MODE = "interactive"
    display_config.POINTER = "encoder"
except Exception:
    display_config = testrunner.display_config


testrunner.run(demo, __file__, disp_config=display_config)
testrunner.devicereset()
