import lvgl as lv



class PlainStyle(lv.style_t):
    name = 'PlainStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(0)

        self.set_outline_width(0)

        self.set_radius(0)



class MonoStyle(lv.style_t):
    name = 'MonoStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(0)
        self.set_border_color(lv.color_make(255,255,255))

        self.set_outline_width(1)
        self.set_outline_color(lv.color_make(255,255,255))

        self.set_shadow_width(0)
        self.set_shadow_offset_x(0)
        self.set_shadow_offset_y(0)

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(255)

        self.set_align(lv.ALIGN.CENTER)



class MonoButtStyle(MonoStyle):
    name = 'MonoButtStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(4)

        self.set_border_width(0)

        self.set_outline_width(1)



class MonoButtPStyle(MonoButtStyle):
    name = 'MonoButtPStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(4)

        self.set_border_width(0)

        self.set_outline_width(2)

        self.set_bg_color(lv.color_make(255,255,255))
        self.set_bg_opa(lv.OPA.COVER)



class MonoArcStyle(lv.style_t):
    name = 'MonoArcStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(0)
        self.set_border_color(lv.color_make(0,255,0))

        self.set_outline_width(0)
        self.set_outline_color(lv.color_white())

        self.set_align(lv.ALIGN.BOTTOM_MID)

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(0)

        self.set_arc_color(lv.color_make(255,255,255))
        self.set_arc_width(8)

        self.set_x(0)



class MonoArcIndStyle(MonoStyle):
    name = 'MonoArcIndStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(2)

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(lv.OPA.COVER)

        self.set_arc_color(lv.color_black())
        self.set_arc_width(4)



class MonoArcKnobStyle(MonoStyle):
    name = 'MonoArcKnobStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_bg_color(lv.color_white())
        self.set_bg_opa(lv.OPA.TRANSP)

        self.set_outline_width(0)



class BoxStyle(lv.style_t):
    name = 'BoxStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(2)

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(0)
        self.set_border_color(lv.color_make(255,255,255))
        self.set_border_side(11)

        self.set_outline_width(0)
        self.set_outline_color(lv.color_make(255,255,255))

        self.set_shadow_width(0)
        self.set_shadow_offset_x(0)
        self.set_shadow_offset_y(0)

        self.set_bg_color(lv.color_hsv_to_rgb(315, 3, 34))
        self.set_bg_opa(0)

        self.set_align(lv.ALIGN.CENTER)

        self.set_x(0)

        self.set_y(0)



class LabelStyle(lv.style_t):
    name = 'LabelStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_align(lv.ALIGN.CENTER)

        self.set_text_color(lv.color_white())
        self.set_text_font(lv.font_montserrat_24)

        self.set_y(0)



class BarStyle(lv.style_t):
    name = 'BarStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(2)

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(1)
        self.set_border_color(lv.color_make(255,255,255))

        self.set_outline_width(1)

        self.set_shadow_width(0)
        self.set_shadow_offset_x(0)
        self.set_shadow_offset_y(0)

        self.set_bg_color(lv.color_make(20, 20, 20))
        self.set_bg_opa(0)

        self.set_align(lv.ALIGN.CENTER)

        self.set_x(0)

        self.set_y(0)



class BarIndStyle(BarStyle):
    name = 'BarIndStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(1)

        self.set_bg_color(lv.color_make(255,255,255))
        self.set_bg_opa(lv.OPA.COVER)



class MonoWifiStyle(lv.style_t):
    name = 'MonoWifiStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(0)
        self.set_border_color(lv.color_make(0,255,0))

        self.set_outline_width(0)
        self.set_outline_color(lv.color_white())

        self.set_align(lv.ALIGN.BOTTOM_MID)

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(0)

        self.set_arc_color(lv.color_make(255,255,255))
        self.set_arc_width(2)

        self.set_x(0)



class MonoWifiIndStyle(MonoWifiStyle):
    name = 'MonoWifiIndStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(lv.OPA.COVER)

        self.set_arc_color(lv.color_black())
        self.set_arc_width(0)



class MonoWifiKnobStyle(MonoStyle):
    name = 'MonoWifiKnobStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_pad_all(0)

        self.set_bg_color(lv.color_white())
        self.set_bg_opa(lv.OPA.TRANSP)

        self.set_outline_width(0)



class ThermStyle(lv.style_t):
    name = 'ThermStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(8)

        self.set_pad_all(0)

        self.set_margin_bottom(0)
        self.set_margin_top(0)
        self.set_margin_left(0)
        self.set_margin_right(0)

        self.set_border_width(1)
        self.set_border_color(lv.color_make(255,255,255))

        self.set_outline_width(0)
        self.set_outline_color(lv.color_white())

        self.set_bg_color(lv.color_make(0,0,0))
        self.set_bg_opa(lv.OPA.COVER)



class ThermIndStyle(ThermStyle):
    name = 'ThermIndStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(0)

        self.set_bg_color(lv.color_make(255,255,255))
        self.set_bg_opa(lv.OPA.COVER)



class ChartStyle(lv.style_t):
    name = 'ChartStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_bg_color(lv.color_black())
        self.set_bg_opa(lv.OPA.TRANSP)

        self.set_border_color(lv.color_black())
        self.set_border_opa(lv.OPA.COVER)
        self.set_border_width(0)



class ChartItemStyle(lv.style_t):
    name = 'ChartItemStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_line_color(lv.color_white())
        self.set_line_opa(lv.OPA.COVER)
        self.set_line_width(2)
        self.set_line_rounded(True)



class ChartIndStyle(lv.style_t):
    name = 'ChartIndStyle'

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.set_radius(lv.RADIUS_CIRCLE)

        self.set_width(1)

        self.set_height(1)

        self.set_bg_opa(lv.OPA.COVER)

        self.set_border_width(0)

        self.set_outline_width(0)
        self.set_outline_pad(0)

        self.set_pad_left(0)
        self.set_pad_right(0)
        self.set_pad_top(0)
        self.set_pad_bottom(0)

styles = [PlainStyle, MonoStyle, MonoButtStyle, MonoButtPStyle, MonoArcStyle, MonoArcIndStyle, MonoArcKnobStyle, BoxStyle, LabelStyle, BarStyle, BarIndStyle, MonoWifiStyle, MonoWifiIndStyle, MonoWifiKnobStyle, ThermStyle, ThermIndStyle, ChartStyle, ChartItemStyle, ChartIndStyle]
