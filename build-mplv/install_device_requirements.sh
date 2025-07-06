#! /bin/bash

cd micropython

unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then

    source tools/ci.sh && ci_esp32_idf_setup
    source tools/ci.sh && ci_esp32_build_common

elif [[ "$unamestr" == 'Darwin' ]]; then


    source tools/ci.sh && ci_esp32_idf_setup
    source tools/ci.sh && ci_esp32_build_common
fi
