#! /bin/bash

cd micropython

unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then

    source tools/ci.sh && ci_stm32_setup

elif [[ "$unamestr" == 'Darwin' ]]; then

    brew install gcc-arm-none-eabi 
    arm-none-eabi-gcc --version
    pip3 install pyelftools
    pip3 install ar
    pip3 install pyhy

fi
