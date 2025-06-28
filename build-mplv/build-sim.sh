
cd micropython 
make -C ports/unix VARIANT_DIR=../../../ports/unix/variants/UNIX-LVGL

cd ..
export SIM=$PWD/micropython/ports/unix/build-UNIX-LVGL/micropython
