# esp-idf download and build
git clone -b v4.4 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
git submodule update --init --recursive
./install.sh
source export.sh
cd ..

# build micropython
make ${MAKEOPTS} -C mpy-cross
make ${MAKEOPTS} -C ports/esp32 submodules
# build GENERIC firmware
make ${MAKEOPTS} -C ports/esp32 \
    FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest.py \
    BOARD=GENERIC
# build GENERIC_OTA firmware
make ${MAKEOPTS} -C ports/esp32 \
    FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest.py \
    BOARD=GENERIC_OTA