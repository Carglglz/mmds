

cd micropython 

make -C ports/stm32 submodules
make -C ports/stm32 BOARD_DIR=../../../ports/stm32/boards/PYBOARD-LVGL

