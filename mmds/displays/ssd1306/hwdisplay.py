import lvgl as lv
from machine import I2C, Pin, ADC
import ssd1306
import framebuf

# import pyb

try:
    import display_config

    DEBUG = display_config.DEBUG
    SENSIBILITY = 10
    if hasattr(display_config, "SENSIBILITY"):
        SENSIBILITY = getattr(display_config, "SENSIBILITY")
except Exception:
    print("display_config NOT FOUND")
    DEBUG = False
    SENSIBILITY = 10


class Device:
    def __init__(self):
        self.user_data = None  # lv indev obj


class PotEncoder:
    def __init__(self, pin=Pin(34)):
        self.adc = ADC(pin)
        self.adc.atten(ADC.ATTN_11DB)
        self._last_v = self.read()

    def read(self):
        return int((self.adc.read() / 4095) * 100)

    def get_step_event(self, sensibility=SENSIBILITY):
        cv = self.read()
        if abs(cv - self._last_v) >= sensibility:
            if cv > self._last_v:
                self._last_v = cv
                return -1  # LEFT
            else:
                self._last_v = cv
                return 1  # RIGHT
        return 0


class Button:
    def __init__(self, outpin=33, inpin=27):
        self.input = Pin(inpin)
        self.input.init(Pin.IN, Pin.PULL_DOWN)

        self.output = Pin(outpin, Pin.OUT)
        self.output.value(1)

    def value(self):
        return self.input.value()


class HwDisplayDriver:
    def __init__(self, width=128, height=64, color_format=lv.COLOR_FORMAT.I1):
        self.width = width
        self.height = height
        self.color_format = color_format
        self.color_depth = lv.color_format_get_bpp(color_format)
        self.color_size = lv.color_format_get_size(color_format)
        self.devices = [Device()]
        self.btn = Button()
        self.pot = PotEncoder()
        self._debug = DEBUG
        self._press_event = False
        self._key_pressed = None
        self.i2c = I2C(scl=Pin(22), sda=Pin(23))
        self.ssd = ssd1306.SSD1306_I2C(width, height, self.i2c)
        self.ssd.fill(0)
        self.ssd.show()
        self.vdisp = width < height
        self.ssd.rotate(True)
        self._disp_buff = None
        self.indev_type = lv.INDEV_TYPE.ENCODER
        if display_config.RENDER_MODE == lv.DISPLAY_RENDER_MODE.PARTIAL:
            self.blit = self.blit_mono_partial
        else:
            self.blit = self.blit_mono_full
        self._display = None

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, x):
        self._debug = x

    def set_frame_buffer(self, fb):
        if self.color_format == lv.COLOR_FORMAT.I1 and (
            display_config.RENDER_MODE == lv.DISPLAY_RENDER_MODE.FULL
        ):
            self._disp_buff = framebuf.FrameBuffer(
                fb[8:], self.width, self.height, framebuf.MONO_HLSB
            )

    def set_display(self, display):
        self._display = display

    def splash(self):
        self.ssd.fill(0)
        self.ssd.fill_rect(50, 20, 32, 32, 1)
        # self.ssd.fill_rect(52, 22, 28, 28, 0)
        self.ssd.vline(59, 28, 28, 0)
        self.ssd.vline(66, 18, 28, 0)
        self.ssd.vline(73, 28, 28, 0)
        self.ssd.fill_rect(77, 46, 2, 4, 0)
        self.ssd.text("MicroPython", 22, 56, 1)
        self.ssd.show()

    def blit_mono_full(self, x1, y1, w, h, buff):
        self.ssd.blit(self._disp_buff, 0, 0)
        self.ssd.show()

    def blit_mono_partial(self, x1, y1, w, h, buff):
        # (buffer, width, height, format)
        self.ssd.blit((buff[8:], w, h, framebuf.MONO_HLSB), x1, y1)
        if self._display:
            if self._display.flush_is_last():
                self.ssd.show()
        else:
            self.ssd.show()

    def read_cb(self, indev, data):
        # return
        try:
            # print("read_cb:")
            if self.btn.value() and not self._press_event:
                self._key_pressed = lv.KEY.ENTER

                data.state = lv.INDEV_STATE.PRESSED
                # data.enc_diff = self._key_pressed
                self._press_event = True
                if self._debug:
                    print("btn press")
                return
            elif not self.btn.value() and self._press_event:
                if self._debug:
                    print("btn release")
                self._press_event = False
                self._key_pressed = lv.KEY.ENTER
                # data.enc_diff = self._key_pressed
                data.state = lv.INDEV_STATE.RELEASED
                return

            # ROT ENCODER

            self._key_pressed = self.pot.get_step_event()
            if self._key_pressed != 0:
                data.enc_diff = self._key_pressed
                # data.state = lv.INDEV_STATE.PRESSED
                # if self._key_pressed in (lv.KEY.PREV, lv.KEY.LEFT):
                if self._key_pressed < 0:
                    if self._debug:
                        print("enc left/prev")
                elif self._key_pressed > 0:
                    if self._debug:
                        print("enc right/next")
                return

        except Exception as e:
            print(e)
