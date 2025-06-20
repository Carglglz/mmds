import lvgl as lv
from machine import I2C
import ssd1306
import framebuf
import sys
import pyb

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
    def __init__(self, pin=pyb.Pin.board.X19):
        self.adc = pyb.ADC(pin)
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


class HwDisplayDriver:
    def __init__(self, width=128, height=64, color_format=lv.COLOR_FORMAT.RGB565):
        self.width = width
        self.height = height
        self.color_format = color_format
        self.color_depth = lv.color_format_get_bpp(color_format)
        self.color_size = lv.color_format_get_size(color_format)
        self.devices = [Device()]
        self.btn = pyb.Switch()
        self.pot = PotEncoder()
        self._debug = DEBUG
        self._press_event = False
        self._key_pressed = None
        self.i2c = I2C("X")
        self.ssd = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.ssd.fill(0)
        self.ssd.show()
        self.vdisp = width < height
        self.ssd.rotate(True)
        self._disp_buff = None
        self.indev_type = lv.INDEV_TYPE.ENCODER
        if color_format == lv.COLOR_FORMAT.RGB565:
            self.blit = self.blit_rgb565
        else:
            self.blit = self.blit_mono

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, x):
        self._debug = x

    def set_frame_buffer(self, fb):
        if self.color_format == lv.COLOR_FORMAT.RGB565:
            self._disp_buff = framebuf.FrameBuffer(
                fb, self.width, self.height // 10, framebuf.RGB565
            )
        elif self.color_format == lv.COLOR_FORMAT.I1:
            # self._disp_buff = fb
            # self._out_buff = bytearray(len(fb[8:]))

            self._fbuff_in = framebuf.FrameBuffer(
                fb[8:], self.width, self.height, framebuf.MONO_HLSB
            )
            # self._fbuff_out = framebuf.FrameBuffer(
            #     self._out_buff, self.width, self.height, framebuf.MONO_VLSB
            # )

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

    def rgb565_to_mono(self, rgb565_buffer, width, height, x_off, y_off):
        """
        Convert RGB565 buffer to monochrome buffer using FrameBuffer

        Args:
            rgb565_buffer: Input buffer of 16-bit RGB565 pixels (bytearray or bytes)
            width: Image width in pixels
            height: Image height in pixels

        """

        # C optimized FrameBuffer functions
        if hasattr(self._disp_buff, "resize"):
            self._disp_buff.resize(width, height)
            self.ssd.blit(self._disp_buff, x_off, y_off)

        else:
            # This is not efficient due to memory allocation --> fragmentation
            self._disp_buff = framebuf.FrameBuffer(
                rgb565_buffer, width, height, framebuf.RGB565
            )

            for y in range(height):
                for x in range(width):
                    pixel = self._disp_buff.pixel(x, y)
                    r = ((pixel >> 11) & 0x1F) << 3  # 5 bits to 8 bits
                    g = ((pixel >> 5) & 0x3F) << 2  # 6 bits to 8 bits
                    b = (pixel & 0x1F) << 3  # 5 bits to 8 bits

                    # Calculate luminance (using approximate weights)
                    luminance = (r * 299 + g * 587 + b * 114) // 1000
                    # if luminance > 0:
                    #     print(f"x:{x}, y:{y}, R:{r}, G:{g}, B:{b}, L:{luminance}")
                    # Set pixel in monochrome buffer (FrameBuffer handles HLSB packing)
                    self.ssd.pixel(
                        x + x_off, y + y_off, 1 if luminance >= threshold else 0
                    )

    def rgb565_to_mono_rot_90(
        self, rgb565_buffer, width, height, x_off, y_off, threshold=128
    ):
        # Create FrameBuffer objects

        # self._disp_buff.resize(width, height)
        self._disp_buff = framebuf.FrameBuffer(
            rgb565_buffer, width, height, framebuf.RGB565
        )
        # Rotate the buffer: process each pixel
        for y in range(height):
            for x in range(width):
                # Translate to new buffer center

                pixel = self._disp_buff.pixel(x, y)

                # Extract RGB components
                r = ((pixel >> 11) & 0x1F) << 3  # 5 bits to 8 bits
                g = ((pixel >> 5) & 0x3F) << 2  # 6 bits to 8 bits
                b = (pixel & 0x1F) << 3  # 5 bits to 8 bits
                # print(f"x:{x}, y:{y}, R:{r}, G:{g}, B:{b}")

                # Calculate luminance (using approximate weights)
                luminance = (r * 299 + g * 587 + b * 114) // 1000

                # if luminance >= threshold:
                #     print(self.ct(x + x_off, y + y_off))

                self.ssd.pixel(
                    *self.ct(x + x_off, y + y_off),
                    1 if luminance >= threshold else 0,
                )

    def ct(self, x, y):
        # 0, 0 -> 127, 0
        # 63, 0 -> 127, 63
        # 63, 127 -> 0, 63
        # 0, 127 -> 0, 0
        _x = 127 - y
        _y = x
        return _x, _y

    def blit_rgb565(self, x1, y1, w, h, buff):
        try:
            # if len(buff) != len(self.disp_mv):
            # print(f"[{x1,y1, w,h}, ")
            if self.vdisp:
                self.rgb565_to_mono_rot_90(buff, w, h, x1, y1, 120)
            else:
                self.rgb565_to_mono(buff, w, h, x1, y1)
            self.ssd.show()
        except Exception as e:
            sys.print_exception(e)

    def blit_mono(self, x1, y1, w, h, buff):
        # FIXME: move ssd.show to final flush if using partial/direct render
        self.ssd.blit(self._fbuff_in, 0, 0)
        self.ssd.show()

    def read_cb(self, indev, data):
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
