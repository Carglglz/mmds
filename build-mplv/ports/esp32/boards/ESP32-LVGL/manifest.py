freeze("$(PORT_DIR)/modules")
include("$(MPY_DIR)/extmod/asyncio")

require("neopixel")
require("mip")
require("ssl")
require("aiorepl")
# LVGL
include("$(MPY_DIR)/../user_modules/lv_binding_micropython/ports/esp32")
# GUI
include("$(MPY_DIR)/../../mmds")
