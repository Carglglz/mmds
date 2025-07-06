set(SDKCONFIG_DEFAULTS

	${CMAKE_CURRENT_LIST_DIR}/sdkconfig.base
	${CMAKE_CURRENT_LIST_DIR}/sdkconfig.board
    boards/sdkconfig.ble
)


if(NOT MICROPY_FROZEN_MANIFEST)
	set(MICROPY_FROZEN_MANIFEST ${CMAKE_CURRENT_LIST_DIR}/manifest.py)
endif()

if(NOT USER_C_MODULES)
    set(USER_C_MODULES ../../../../user_modules/micropythonesp32_lvgl.cmake)
endif()


if(NOT DEFINED LV_CONF_DIR)
    set(LV_CONF_DIR ${CMAKE_CURRENT_LIST_DIR})
endif()

if(NOT DEFINED LV_CONF_PATH)
    set(LV_CONF_PATH ${LV_CONF_DIR}/lv_conf_v9_3.h)
endif()
