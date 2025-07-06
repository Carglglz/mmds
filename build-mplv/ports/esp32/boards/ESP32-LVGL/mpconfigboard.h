// Both of these can be set by mpconfigboard.cmake if a BOARD_VARIANT is
// specified.

#ifndef MICROPY_HW_BOARD_NAME
#define MICROPY_HW_BOARD_NAME "Generic ESP32 module"
#endif

#ifndef MICROPY_HW_MCU_NAME
#define MICROPY_HW_MCU_NAME "ESP32-LVGL-DEV"
#endif

#define MICROPY_GC_INITIAL_HEAP_SIZE (64 * 1024)


#include "lv_conf_v9_3.h"
