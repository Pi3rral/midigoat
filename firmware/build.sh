source esp-idf/export.sh
make ${MAKEOPTS} -C mpy-cross
make ${MAKEOPTS} -C ports/esp32 submodules
# build GENERIC firmware with basic manifest
# make ${MAKEOPTS} -C ports/esp32 \
#     FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest.py \
#     BOARD=GENERIC
# build GENERIC_OTA firmware
make ${MAKEOPTS} -C ports/esp32 \
    FROZEN_MANIFEST=$(pwd)/ports/esp32/boards/manifest_midigoat.py \
    BOARD=GENERIC_OTA
