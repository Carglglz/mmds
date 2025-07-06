

cd micropython 

make -C ports/esp32 submodules
make -C ports/esp32 BOARD_DIR=../../../ports/esp32/boards/ESP32-LVGL

