import lvgl as lv
from machine import I2C
import ssd1306
import framebuf
import sys

import pyb

try:
    import display_config

    DEBUG = display_config.DEBUG
except Exception:
    DEBUG = False


class Device:
    def __init__(self):
        self.user_data = None  # lv indev obj


class PotEncoder:
    def __init__(self, pin=pyb.Pin.board.X19):
        self.adc = pyb.ADC(pin)
        self._last_v = self.read()

    def read(self):
        return int((self.adc.read() / 4095) * 100)

    def get_key_event(self, sensibility=10):
        cv = self.read()
        if abs(cv - self._last_v) >= sensibility:
            if cv > self._last_v:
                self._last_v = cv
                return lv.KEY.LEFT
            else:
                self._last_v = cv
                return lv.KEY.RIGHT


class HwDisplayDriver:
    def __init__(self, width=128, height=64, color_format=lv.COLOR_FORMAT.I1):
        self.width = width
        self.height = height
        self.color_depth = lv.color_format_get_bpp(color_format)
        self.color_size = lv.color_format_get_size(color_format)
        self.devices = [Device()]
        self.btn = pyb.Switch()
        self.pot = PotEncoder()
        self._debug = False
        self._press_event = False
        self._key_pressed = None
        self._x = int(width / 2)
        self.__y = self.gen_y()

        self.i2c = I2C("X")
        self.ssd = ssd1306.SSD1306_I2C(128, 64, self.i2c)

        self.ssd.fill(0)
        self.ssd.show()
        self.vdisp = width < height
        self.ssd.rotate(True)
        # buffer_size = width * (self.color_depth // 8) * (height // 10)
        # print(buffer_size)
        # self.disp_buff = bytearray(buffer_size)
        # self.disp_mv = memoryview(self.disp_buff)

        # self.async_indev_start()

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, x):
        self._debug = x

    def gen_y(self):
        for i in range(0, self.height * 2, int(self.height / 6)):
            yield i

    def get_y(self):
        self._y = next(self.__y)

    def rgb565_to_mono_hmsb(self, rgb565_buffer, width, height, threshold=128):
        """
        Convert RGB565 buffer to monochrome HMSB buffer.

        Args:
            rgb565_buffer: Input buffer of 16-bit RGB565 pixels
            width: Image width in pixels
            height: Image height in pixels
            threshold: Luminance threshold (0-255) for monochrome conversion

        Returns:
            bytearray: Monochrome HMSB buffer
        """
        # Calculate output buffer size (1 bit per pixel, 8 pixels per byte)
        output_size = (width * height + 7) // 8
        mono_buffer = bytearray(output_size)

        for y in range(height):
            for x in range(width):
                # Get RGB565 pixel (16-bit)
                pixel = rgb565_buffer[(y * width + x) * 2] | (
                    rgb565_buffer[(y * width + x) * 2 + 1] << 8
                )

                # Extract RGB components
                r = ((pixel >> 11) & 0x1F) << 3  # 5 bits to 8 bits
                g = ((pixel >> 5) & 0x3F) << 2  # 6 bits to 8 bits
                b = (pixel & 0x1F) << 3  # 5 bits to 8 bits

                # Calculate luminance (using approximate weights)
                luminance = (r * 299 + g * 587 + b * 114) // 1000

                # Determine bit position
                pixel_index = y * width + x
                byte_index = pixel_index // 8
                bit_index = 7 - (pixel_index % 8)  # HMSB: most significant bit first

                # Set bit if luminance is above threshold
                if luminance >= threshold:
                    mono_buffer[byte_index] |= 1 << bit_index

        return mono_buffer

    def rgb565_to_mono_hlsb(
        self, rgb565_buffer, width, height, x_off, y_off, threshold=128
    ):
        """
        Convert RGB565 buffer to monochrome HLSB buffer using FrameBuffer and memoryview.

        Args:
            rgb565_buffer: Input buffer of 16-bit RGB565 pixels (bytearray or bytes)
            width: Image width in pixels
            height: Image height in pixels
            threshold: Luminance threshold (0-255) for monochrome conversion

        Returns:
            framebuf.FrameBuffer: Monochrome HLSB buffer
        """
        # Calculate output buffer size (1 bit per pixel, 8 pixels per byte)
        # output_size = (width * height + 7) // 8
        # mono_buffer = bytearray(output_size)

        # Create FrameBuffer objects
        rgb_fb = framebuf.FrameBuffer(rgb565_buffer, width, height, framebuf.RGB565)
        # mono_fb = framebuf.FrameBuffer(mono_buffer, width, height, framebuf.MONO_HLSB)

        # # Use memoryview for efficient buffer access
        # rgb_mv = memoryview(rgb565_buffer)

        for y in range(height):
            for x in range(width):
                # Get RGB565 pixel (16-bit) using FrameBuffer
                # print(x, y)
                pixel = rgb_fb.pixel(x, y)

                # Extract RGB components
                r = ((pixel >> 11) & 0x1F) << 3  # 5 bits to 8 bits
                g = ((pixel >> 5) & 0x3F) << 2  # 6 bits to 8 bits
                b = (pixel & 0x1F) << 3  # 5 bits to 8 bits
                # print(f"x:{x}, y:{y}, R:{r}, G:{g}, B:{b}")

                # Calculate luminance (using approximate weights)
                luminance = (r * 299 + g * 587 + b * 114) // 1000
                # if luminance >= threshold:
                #     print(x + x_off, y + y_off)
                # Set pixel in monochrome buffer (FrameBuffer handles HLSB packing)
                self.ssd.pixel(x + x_off, y + y_off, 1 if luminance >= threshold else 0)

        # return mono_fb

    def rgb565_to_mono_rot_90_hlsb(
        self, rgb565_buffer, width, height, x_off, y_off, threshold=128
    ):
        """
        Convert RGB565 buffer to monochrome HLSB buffer using FrameBuffer and memoryview.

        Args:
            rgb565_buffer: Input buffer of 16-bit RGB565 pixels (bytearray or bytes)
            width: Image width in pixels
            height: Image height in pixels
            threshold: Luminance threshold (0-255) for monochrome conversion

        Returns:
            framebuf.FrameBuffer: Monochrome HLSB buffer
        """
        # Calculate output buffer size (1 bit per pixel, 8 pixels per byte)
        # output_size = (width * height + 7) // 8
        # mono_buffer = bytearray(output_size)

        # Create FrameBuffer objects
        rgb_fb = framebuf.FrameBuffer(rgb565_buffer, width, height, framebuf.RGB565)
        # Rotate the buffer: process each pixel
        for y in range(height):
            for x in range(width):
                # Translate to new buffer center

                pixel = rgb_fb.pixel(x, y)

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

    def blit(self, x1, y1, w, h, buff):
        try:
            # if len(buff) != len(self.disp_mv):
            # print(f"[{x1,y1, w,h}, ")
            if self.vdisp:
                self.rgb565_to_mono_rot_90_hlsb(buff, w, h, x1, y1, 120)
            else:
                self.rgb565_to_mono_hlsb(buff, w, h, x1, y1, 120)
            self.ssd.show()
        except Exception as e:
            sys.print_exception(e)

    def read_cb(self, indev, data):
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

        self._key_pressed = self.pot.get_key_event()
        if self._key_pressed:
            data.enc_diff = self._key_pressed
            # data.state = lv.INDEV_STATE.PRESSED
            if self._key_pressed in (lv.KEY.PREV, lv.KEY.LEFT):
                if self._debug:
                    print("enc left/prev")
            elif self._key_pressed in (lv.KEY.NEXT, lv.KEY.RIGHT):
                if self._debug:
                    print("enc right/next")
            return
