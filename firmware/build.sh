source esp-idf/export.sh
make ${MAKEOPTS} -C mpy-cross
make ${MAKEOPTS} -C ports/esp32 submodules
# make ${MAKEOPTS} -C ports/esp32 \
#     USER_C_MODULES=../../../examples/usercmodule/micropython.cmake \
#     FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest_test.py
make ${MAKEOPTS} -C ports/esp32 \
    FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest_midigoat.py \
    BOARD=GENERIC_OTA