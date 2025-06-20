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
    sys.path.append(f"{root_testdir}/sim")


from gui import testrunner
from gui.ui.monoc import StatusBar, Thermometer, MMenu, MChart, Mlabel, Marc  # noqa
from gui.mgui import Clock, TMP36
from gui.callbacks import callback
import time
import lvgl as lv

# This is a status bar test


async def test_gui(scr, display=None, adc=None, temp=None, dt=20, buzz=None):
    print("MONO GUI TEST:")
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

    arc_setting = Marc(scr, w=44, h=44, rng=(0, 100), symb="", scr=False)
    arc_setting.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)
    arc_setting.lab.align(lv.ALIGN.RIGHT_MID, -10, 10)
    arc_setting.add_flag(lv.obj.FLAG.HIDDEN)
    arc_setting.lab.add_flag(lv.obj.FLAG.HIDDEN)

    # MENU
    menu = MMenu(scr, scr=False, sd=buzz)
    menu.apps[menu.btn1] = [thm, thm_lab]
    menu.apps[menu.btn2] = [plot, plot.lab, plot.graph]
    menu.apps[menu.btn3] = [info, arc_setting, arc_setting.lab]

    # INDEV GROUP
    wgroup = lv.group_create()
    wgroup.add_obj(menu.btn1)
    wgroup.add_obj(menu.btn2)
    wgroup.add_obj(menu.btn3)
    display.indev.set_group(wgroup)

    if buzz:

        @callback
        def focus_cb(group):
            buzz.beep()

        wgroup.set_focus_cb(focus_cb)

        @callback.value_changed(arc_setting)
        def set_fq(event):
            v = arc_setting.get_value()
            fq = int(4400 * (v / 100))
            if abs(fq - buzz.fq) > 200:
                buzz.fq = fq
                buzz.beep()

    # APP EVENT LOOP
    async def app_event_loop(dt_loop_ms=1000):
        try:
            t0 = time.time()
            while (time.time() - t0) * 1000 < dt_loop_ms:
                i = int((adc.read() / 4095) * 100)
                tmp = ts.read_tmp()
                sb.batt.set_bvalue(100 - i)
                sb.wifi.set_wvalue(-i)
                sb.clock.set_text(clk.time())
                if menu._backmode:
                    if menu.btns[menu.selected] == menu.btn3:
                        arc_setting.set_mvalue(100 - i)

                        arc_setting.send_event(lv.EVENT.VALUE_CHANGED, None)

                    if menu.btns[menu.selected] == menu.btn1:
                        thm.set_tvalue(int(tmp))
                        thm_lab.set_text(f"{tmp:.1f} C")

                plot.update(scale=10)

                await asyncio.sleep_ms(dt)

        except Exception as e:
            print(e)

    async def select_app(name, menu, btn):
        print(f"MONO GUI {name.upper()}")
        btn.send_event(lv.EVENT.FOCUSED, None)

        await app_event_loop(1000)

        btn.send_event(lv.EVENT.PRESSED, None)
        btn.send_event(lv.EVENT.RELEASED, None)

        await app_event_loop(2000)

        menu.send_event(lv.EVENT.PRESSED, None)

        await app_event_loop(1000)

        btn.send_event(lv.EVENT.DEFOCUSED, None)

    # MENU
    print("MONO GUI MENU")
    await app_event_loop(2000)

    for name, btn in [
        ("Thermometer", menu.btn1),
        ("Chart", menu.btn2),
        ("Settings", menu.btn3),
    ]:
        await select_app(name, menu, btn)


__file__ = globals().get("__file__", "test")

try:
    import display_config
    import board_config

    display_config.MODE = "interactive"
    display_config.POINTER = "sim"
except Exception:
    display_config = testrunner.display_config


testrunner.run(test_gui, __file__, disp_config=display_config, **board_config.conf)
testrunner.devicereset()
