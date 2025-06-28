

### LVGL IO


Integrate display/indev drivers with lvgl, see `mmds/displays/ssd1306/hwdisplay.py` for [reference](../mmds/displays/ssd1306/hwdisplay.py)

#### Display driver: 

To add a driver create a dir in `mmds/displays`, e.g. `mydriver` and add a `hwdisplay.py`

which requires a `HwDisplayDriver` with the following signature

```py
class HwDisplayDriver:
    def __init__(self, width=128, height=64, color_format=lv.COLOR_FORMAT.RGB565):
```
and a `blit` method with the following signature 

```py
   def blit(self, x1, y1, w, h, buff):

```

that will be called by lvgl `flush_cb`, see [flush callback](https://docs.lvgl.io/master/details/main-modules/display/setup.html#flush-callback)

then  `display_config.py` will set display configurations options i.e. display width/height, color_format, render mode, indev type, etc 

```py

import lvgl as lv

MODE = "interactive"
INDEV = "encoder"
WIDTH = 128
HEIGHT = 64
COLOR_FORMAT = lv.COLOR_FORMAT.I1
RENDER_MODE = lv.DISPLAY_RENDER_MODE.PARTIAL
SHOW_INFO = True
```
for more information check lvgl display [ docs ](https://docs.lvgl.io/master/details/main-modules/display/setup.html)



#### Indev driver: 

To allow lvgl read events from input devices, using lvgl indev read callback, `HwDisplayDriver` requires a 
`read_cb` method with the following signature:

```py

    def read_cb(self, indev, data):
```

that populates `data` with the appropriate events, e.g.   

```py

    def read_cb(self, indev, data):
        try:
            if self.btn.value() and not self._press_event:
                self._key_pressed = lv.KEY.ENTER

                data.state = lv.INDEV_STATE.PRESSED
                self._press_event = True
                if self._debug:
                    print("btn press")
                return
            elif not self.btn.value() and self._press_event:
                if self._debug:
                    print("btn release")
                self._press_event = False
                self._key_pressed = lv.KEY.ENTER
                data.state = lv.INDEV_STATE.RELEASED
                return

            # ROT ENCODER

            self._key_pressed = self.pot.get_step_event()
            if self._key_pressed != 0:
                data.enc_diff = self._key_pressed
                if self._key_pressed < 0:
                    if self._debug:
                        print("enc left/prev")
                elif self._key_pressed > 0:
                    if self._debug:
                        print("enc right/next")
                return

        except Exception as e:
            print(e)
```

for more information check indev [docs](https://docs.lvgl.io/master/details/main-modules/indev.html)
