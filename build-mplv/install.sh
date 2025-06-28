#! /bin/bash

unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then
    echo "Installing linux requirements..."
    sh install_requirements_linux.sh
elif [[ "$unamestr" == 'Darwin' ]]; then

    echo "Installing macos requirements..."
    sh install_requirements_macos.sh
fi

echo "Initiating submodules..."
git submodule update --init -f --remote


echo "Initiating lv_binding submodules..."

git submodule update --init --recursive ./user_modules/lv_binding_micropython

cd ./micropython

make -C mpy-cross

make -C ports/unix submodules

make -C ports/unix deplibs
