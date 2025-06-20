import lvgl as lv
from .style_monoc import *
from ..callbacks import callback


class MonoChromeScreen(lv.obj):
    def __init__(self, parent, w=128, h=64):
        super().__init__(parent)
        self.add_style(PlainStyle(), 0)
        self.set_size(w, h)
        self.center()
        self.set_style_bg_color(lv.color_black(), 0)


class Mwidget(lv.obj):
    def __init__(self, parent, w=20, h=20):
        self.scr = MonoChromeScreen(parent)
        super().__init__(self.scr)

        self.add_style(PlainStyle(), 0)
        self.set_size(w, h)
        self.center()


class Mbar(lv.bar):
    def __init__(self, parent, w=80, h=5, rng=(0, 100), scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
            self.lab = lv.label(self.scr)
        else:
            super().__init__(parent)

            self.lab = lv.label(parent)

        self.add_style(MonoStyle(), 0)
        self.set_size(w, h)
        self.center()
        self.lab.set_text(f"{0} %")
        self.lab.set_style_text_color(lv.color_white(), 0)
        self.lab.align(lv.ALIGN.TOP_MID, 5, 5)

        self.set_range(*rng)
        self.set_style_bg_color(lv.color_white(), lv.PART.INDICATOR)
        self.set_value(rng[0], True)

    def set_mvalue(self, v):
        self.set_value(v, True)

        self.lab.set_text(f"{v} %")


class Marc(lv.arc):
    def __init__(self, parent, w=60, h=60, rng=(0, 100), symb="%", scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
            self.lab = lv.label(self.scr)
        else:
            super().__init__(parent)

            self.lab = lv.label(parent)
        self.symb = symb
        self.add_style(MonoArcStyle(), lv.PART.MAIN)
        self.add_style(MonoArcIndStyle(), lv.PART.INDICATOR)
        self.add_style(MonoArcKnobStyle(), lv.PART.KNOB)
        self.set_size(w, h)
        # self.center()
        self.set_mode(lv.arc.MODE.REVERSE)
        self.lab.set_text(f"{0}%")
        self.lab.set_style_text_color(lv.color_white(), 0)
        self.lab.align(lv.ALIGN.CENTER, 0, 2)

        # self.set_style_bg_color(lv.color_white(), lv.PART.INDICATOR)
        self.set_value(rng[0])
        self.set_range(*rng)
        self.min, self.max = rng

    def set_mvalue(self, v):
        self.set_value(self.max - v)

        self.lab.set_text(f"{v} {self.symb}")


class Mbutton(lv.button):
    def __init__(
        self, parent, w=60, h=22, text="Test", scr=True, pc=False, focus=False, sd=None
    ):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(MonoButtStyle(), lv.PART.MAIN)
        self.add_style(MonoButtPStyle(), lv.PART.MAIN | lv.STATE.PRESSED)
        if focus:
            self.add_style(MonoButtPStyle(), lv.PART.MAIN | lv.STATE.FOCUSED)

        self._focus = focus
        self.set_size(w, h)
        self.lab = lv.label(self)
        self.lab.set_text(text)

        self.name = text
        self.lab.center()
        self._state = 0
        self._np = 0
        self._press_count = pc
        self.sd = sd

        @callback.pressed(self)
        def _bp(event):
            print(f"btn {self.name} pressed")
            if not self._focus:
                self.lab.set_style_text_color(lv.color_black(), 0)
            if self._press_count:
                self._np += 1
            if self.sd:
                self.sd.beep()

        @callback.released(self)
        def _br(event):
            print(f"btn {self.name} released")
            if not self._focus:
                self.lab.set_style_text_color(lv.color_white(), 0)

        @callback.focused(self)
        def _bf(event):
            # print(f"btn {self.name} focused")
            if self._focus:
                self.lab.set_style_text_color(lv.color_black(), 0)

            # if self.sd:
            #     self.sd.beep()

        @callback.defocused(self)
        def _bd(event):
            # print(f"btn {self.name} defocused")
            if self._focus:
                self.lab.set_style_text_color(lv.color_white(), 0)

        if not focus:
            self.lab.set_style_text_color(lv.color_white(), 0)

    def toggle(self):
        if not self._state:
            self.set_state(lv.STATE.CHECKED, True)
            self.lab.set_style_text_color(lv.color_black(), 0)

        else:
            self.set_state(lv.STATE.CHECKED, False)
            self.lab.set_style_text_color(lv.color_white(), 0)

        self._state = not self._state

    def check(self):
        if not self._state:
            self.toggle()

    def uncheck(self):
        if self._state:
            self.toggle()


class BatteryBar(lv.bar):
    def __init__(self, parent, w=20, h=10):
        super().__init__(parent)
        self.set_size(w, h)
        # self.lab = lv.label(self)

        # self.lab.set_text('60%')

        # self.lab.add_style(LabelStyle(), lv.PART.MAIN)


class BatteryCap(lv.obj):
    def __init__(self, parent, w=2, h=4, r=1):
        super().__init__(parent)
        self.set_style_width(w, 0)
        self.set_style_height(h, 0)
        self.set_style_radius(r, 0)


class Battery(lv.obj):
    def __init__(self, parent, w=18, h=10, vert=False, pct=False, scr=True):
        if w // h < 2:
            h = w // 2
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(BoxStyle(), lv.PART.MAIN)
        self._vert = vert

        if pct:
            self.bpct = lv.label(self)
            self.bpct.set_text("100%")
            self.bpct.set_style_text_color(lv.color_white(), 0)
            if not vert:
                self.bpct.align(lv.ALIGN.LEFT_MID, 2, 1)
            else:
                self.bpct.align(lv.ALIGN.CENTER, 4, 0)
        if vert:
            if pct:
                # self.set_size(h + 2, w + 36)

                self.set_size(w + 30, h + 8)
            else:
                # self.set_size(h, w - 2)

                self.set_size(w, h + 8)
            self.ind = BatteryBar(self, h, w - 4)
            self.cap = BatteryCap(self, h=w // 14, w=h // 3)
            self.cap.align(lv.ALIGN.TOP_MID, 0, 0)
            # if pct:
        else:
            if pct:
                self.set_size(w + 38, h + 2)
            else:
                self.set_size(w, h)

            self.ind = BatteryBar(self, w - 2, h)

            self.cap = BatteryCap(self, w=w // 14, h=h // 3)
            self.cap.align(lv.ALIGN.RIGHT_MID, -1, 0)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        self.set_state(lv.STATE.CHECKED, False)

        self.ind.set_value(60, False)

        self.ind.add_style(BarStyle(), lv.PART.MAIN)

        self.ind.add_style(BarIndStyle(), lv.PART.INDICATOR)
        if pct:
            if not vert:
                self.ind.align(lv.ALIGN.RIGHT_MID, -2, 0)
            else:
                self.ind.align(lv.ALIGN.TOP_RIGHT, -2, 2)

                self.cap.align(lv.ALIGN.TOP_RIGHT, -h // 2, 1)
        else:
            if not vert:
                self.ind.align(lv.ALIGN.LEFT_MID, 0, 0)
            else:
                self.ind.align(lv.ALIGN.TOP_RIGHT, -2, 2)

                self.cap.align(lv.ALIGN.TOP_RIGHT, -h // 2, 1)
        # @callback.value_changed(self.ind)
        # def batt_val_update(event):
        #     self.ind.lab.set_text(str(self.ind.get_value()) + "%")

    def set_bvalue(self, val):
        self.ind.set_value(val, False)
        if hasattr(self, "bpct"):
            self.bpct.set_text(f"{val}%")
            if not self._vert:
                self.bpct.align(lv.ALIGN.LEFT_MID, (4 - len(f"{val}%")) * 3, 1)
            else:
                self.bpct.align(lv.ALIGN.LEFT_MID, (4 - len(f"{val}%")) * 3, 1)


class WifiInd(lv.obj):
    def __init__(self, parent, w=20, h=20, scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(BoxStyle(), lv.PART.MAIN)

        self.set_size(w, h)
        self.remove_flag(lv.obj.FLAG.SCROLLABLE)

        self.l1 = lv.arc(self)

        self.l1.add_style(MonoWifiStyle(), lv.PART.MAIN)
        self.l1.add_style(MonoWifiIndStyle(), lv.PART.INDICATOR)
        self.l1.add_style(MonoWifiKnobStyle(), lv.PART.KNOB)
        self.l1.set_size(w - 2, h - 2)
        self.l1.center()
        self.l1.set_value(0)
        self.l1.set_bg_angles(220, 320)
        self.l1.set_mode(lv.arc.MODE.REVERSE)

        self.l1.align(lv.ALIGN.TOP_MID, 0, 3)

        self.l2 = lv.arc(self)

        self.l2.add_style(MonoWifiStyle(), lv.PART.MAIN)
        self.l2.add_style(MonoWifiIndStyle(), lv.PART.INDICATOR)
        self.l2.add_style(MonoWifiKnobStyle(), lv.PART.KNOB)
        self.l2.set_size(w - 3, h - 3)
        self.l2.align(lv.ALIGN.CENTER, 0, 5)
        self.l2.set_value(0)
        self.l2.set_bg_angles(245, 295)
        self.l2.set_mode(lv.arc.MODE.REVERSE)

        self.l3 = lv.arc(self)

        self.l3.add_style(MonoWifiStyle(), lv.PART.MAIN)
        self.l3.add_style(MonoWifiIndStyle(), lv.PART.INDICATOR)
        self.l3.add_style(MonoWifiKnobStyle(), lv.PART.KNOB)
        self.l3.set_size(w - 2, h - 2)
        self.l3.align(lv.ALIGN.CENTER, 0, 10)
        self.l3.set_value(0)
        self.l3.set_bg_angles(270, 272)
        self.l3.set_mode(lv.arc.MODE.REVERSE)
        self.set_wvalue(-20)

    def set_wvalue(self, rssi):
        if rssi >= -30:
            self.l1.remove_flag(lv.obj.FLAG.HIDDEN)
            self.l2.remove_flag(lv.obj.FLAG.HIDDEN)
        elif rssi < -30 and rssi >= -70:
            self.l1.add_flag(lv.obj.FLAG.HIDDEN)
            self.l2.remove_flag(lv.obj.FLAG.HIDDEN)
        elif rssi < -70:
            self.l1.add_flag(lv.obj.FLAG.HIDDEN)
            self.l2.add_flag(lv.obj.FLAG.HIDDEN)


class StatusBar(lv.obj):
    def __init__(self, parent, w=128, h=16, scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(BoxStyle(), lv.PART.MAIN)

        self.set_flex_flow(lv.FLEX_FLOW.ROW_REVERSE)

        self.set_flex_align(
            lv.FLEX_ALIGN.END,
            lv.FLEX_ALIGN.CENTER,
            lv.FLEX_ALIGN.CENTER,
        )
        self.set_size(w, h)
        self.set_style_pad_column(2, 0)
        self.set_style_pad_top(1, 0)
        self.set_style_pad_right(1, 0)
        self.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.align(lv.ALIGN.TOP_MID, 0, 0)

        self.clock = lv.label(self)

        self.clock.add_style(LabelStyle(), lv.PART.MAIN)
        self.clock.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
        self.clock.set_text("00:00")
        self.batt = Battery(self, vert=False, pct=False, scr=False)
        self.wifi = WifiInd(self, scr=False)

        self.ble = lv.label(self)
        self.ble.set_text(lv.SYMBOL.BLUETOOTH)

        self.ble.set_style_text_color(lv.color_white(), 0)


class Thermometer(lv.obj):
    def __init__(self, parent, w=30, h=50, rng=(0, 100), scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(BoxStyle(), lv.PART.MAIN)

        self.set_size(w, h)
        self.add_flag(lv.obj.FLAG.CLICKABLE)

        self.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.set_state(lv.STATE.CHECKED, False)

        self.ind = BatteryBar(self, w - 20, h - 15)
        self.ind.set_range(*rng)

        self.cap = BatteryBar(self, w=w - 14, h=h // 3)
        self.cap.align(lv.ALIGN.BOTTOM_MID, 0, -2)
        self.cap.add_style(ThermStyle(), lv.PART.MAIN)
        self.cap.add_style(ThermIndStyle(), lv.PART.INDICATOR)
        self.cap.set_orientation(lv.bar.ORIENTATION.VERTICAL)
        self.cap.set_value(50, False)

        self.ind.add_style(BarStyle(), lv.PART.MAIN)
        self.ind.add_style(BarIndStyle(), lv.PART.INDICATOR)

        self.ind.align(lv.ALIGN.TOP_MID, 0, 0)
        # @callback.value_changed(self.ind)
        # def batt_val_update(event):
        #     self.ind.lab.set_text(str(self.ind.get_value()) + "%")
        self._th = rng[-1] // 4
        self.ind.set_range(self._th, rng[-1])

        self.cap.set_range(rng[0], self._th)
        self.set_tvalue(40)

    def set_tvalue(self, val):
        if val >= self._th:
            self.cap.set_value(self._th, False)
            self.ind.set_value(val, False)
        else:
            self.ind.set_value(self._th, False)

            self.cap.set_value(val, False)


class Mlabel(lv.label):
    def __init__(self, parent, text="24", scr=True):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(LabelStyle(), lv.PART.MAIN)
        self.set_text(text)


class MMenu(lv.obj):
    def __init__(self, parent, w=127, h=44, scr=True, sd=None):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)

        else:
            super().__init__(parent)

        self.sd = sd
        parent.add_flag(lv.obj.FLAG.CLICKABLE)

        @callback.pressed(parent, self)
        def _back(event):
            if self._backmode:
                print("back")
                self.press()

        self.add_style(BoxStyle(), lv.PART.MAIN)

        self.set_flex_flow(lv.FLEX_FLOW.ROW)

        self.set_flex_align(
            lv.FLEX_ALIGN.SPACE_AROUND,
            lv.FLEX_ALIGN.SPACE_AROUND,
            lv.FLEX_ALIGN.SPACE_AROUND,
        )
        self.set_size(w, h)
        self.set_style_pad_column(15, 0)
        self.set_style_pad_top(0, 0)
        self.set_style_pad_right(5, 0)
        self.set_style_pad_left(5, 0)
        self.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        self.btn1 = Mbutton(
            self, w=20, h=20, text=lv.SYMBOL.PLAY, scr=False, focus=True, sd=sd
        )
        self.btn2 = Mbutton(
            self, w=20, h=20, text=lv.SYMBOL.AUDIO, scr=False, focus=True, sd=sd
        )
        self.btn3 = Mbutton(
            self, w=20, h=20, text=lv.SYMBOL.SETTINGS, scr=False, focus=True, sd=sd
        )

        self.btns = [self.btn1, self.btn2, self.btn3]
        self.apps = {}
        self.selected = 0
        self._backmode = 0
        self.app = None

        @callback.pressed(*self.btns)
        def _press(event):
            self.selected = self.btns.index(event.get_current_target_obj())

            print(f"btn {self.btns[self.selected].name} pressed")
            self.btns[self.selected].lab.set_style_text_color(lv.color_black(), 0)
            self.press()
            # if self.sd:
            #     self.sd.beep()

        # self.btn1.toggle()

    def select(self, n):
        for i, btn in enumerate(self.btns):
            if i == n:
                btn.check()
                self.selected = i
            else:
                btn.uncheck()

    def show(self, b):
        if b:
            self.remove_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.add_flag(lv.obj.FLAG.HIDDEN)

    def press(self):
        if not self._backmode:
            self.app = self.apps.get(self.btns[self.selected], None)
            if self.app:
                self.show(False)
                for obj in self.app:
                    obj.remove_flag(lv.obj.FLAG.HIDDEN)
        else:
            if self.app:
                self.show(True)
                for obj in self.app:
                    obj.add_flag(lv.obj.FLAG.HIDDEN)
        self._backmode = not self._backmode


class MChart(lv.obj):
    def __init__(
        self,
        parent,
        w=127,
        h=44,
        y_range=(0, 100),
        y_offset=0,
        graph_res=None,
        time_res=30,
        time_dt=1,
        symb="C",
        scr=True,
    ):
        if scr:
            self.scr = MonoChromeScreen(parent)
            super().__init__(self.scr)
        else:
            super().__init__(parent)

        self.add_style(BoxStyle(), lv.PART.MAIN)

        if graph_res is None:
            graph_res = time_res // time_dt
            graph_res = min(w, graph_res)

        self.symb = symb
        self._y_offset = y_offset
        self.set_size(w, h)
        self.align(lv.ALIGN.BOTTOM_MID, 0, -1)
        self.lab = lv.label(self)
        self.lab.add_style(LabelStyle(), lv.PART.MAIN)
        self.lab.set_text("?")
        self.lab.align(lv.ALIGN.TOP_MID, 0, 0)
        self.lab.set_style_text_font(lv.font_montserrat_16, 0)
        self.graph = lv.chart(self)
        self.graph.set_width(w - 2)
        self.graph.set_height(h)
        self.graph.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.graph.set_type(lv.chart.TYPE.LINE)
        self.graph.set_point_count(graph_res - 1)
        self.graph.set_div_line_count(0, 0)
        self.graph.set_axis_range(lv.chart.AXIS.PRIMARY_Y, *y_range)
        self.graph_series_1 = self.graph.add_series(
            lv.color_white(), lv.chart.AXIS.PRIMARY_Y
        )

        self._values = [0 for i in range(graph_res)]
        self.graph.set_series_ext_y_array(self.graph_series_1, self._values)
        self.graph.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
        self.graph.add_style(ChartStyle(), lv.PART.MAIN)

        self.graph.add_style(ChartItemStyle(), lv.PART.ITEMS)

        self.graph.add_style(ChartIndStyle(), lv.PART.INDICATOR)

        self.graph.set_point_count(len(self._values) - 1)

    def set_data_func(self, func):
        self._get_new_value = func

    def update(self, val=None, scale=100):
        if val is None:
            val = self._get_new_value()
        self.lab.set_text(f"{val:.1f} {self.symb}")
        self.graph.set_next_value(
            self.graph_series_1, int(val * scale) - self._y_offset
        )


widget = Mlabel
