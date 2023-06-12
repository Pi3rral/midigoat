FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive


SHELL ["/bin/bash", "-c"] 

USER root

RUN apt-get update \
    && apt-get install -y \
    cmake \
    git \
    python3 \
    python3-pip \
    libusb-1.0-0

ARG MICROPYTHON_DIR=/micropython
ARG MICROPYTHON_VERSION=v1.20.0

RUN git clone -b ${MICROPYTHON_VERSION} https://github.com/micropython/micropython.git ${MICROPYTHON_DIR}

WORKDIR ${MICROPYTHON_DIR}

ENV MICROPYTHON_DIR=${MICROPYTHON_DIR}

COPY firmware/setup.sh ${MICROPYTHON_DIR}/setup.sh
RUN ./setup.sh

# Copy libraries to be added to the firmware
## Microdot
COPY libs/microdot ${MICROPYTHON_DIR}/ports/esp32/modules/microdot
## Adafruit MIDI
COPY libs/Adafruit_CircuitPython_MIDI/adafruit_midi ${MICROPYTHON_DIR}/ports/esp32/modules/adafruit_midi
## LCD library
COPY libs/lcd ${MICROPYTHON_DIR}/ports/esp32/modules/lcd

# Copy manifest and inisetup for "blank" build
COPY firmware/manifest.py ${MICROPYTHON_DIR}/ports/esp32/boards/manifest_midigoat.py
COPY firmware/inisetup.py ${MICROPYTHON_DIR}/ports/esp32/modules/inisetup.py

# build vanilla first to re-use docker layer
# RUN source tools/ci.sh && ci_esp32_idf44_setup
COPY firmware/build.sh ${MICROPYTHON_DIR}/midigoat_build.sh

RUN ./midigoat_build.sh

# Copy midicontroller application
COPY src/midicontroller/ ${MICROPYTHON_DIR}/ports/esp32/modules/midicontroller/
# COPY src/main.py ${MICROPYTHON_DIR}/ports/esp32/modules/boot.py

# build with custom code
RUN ./midigoat_build.sh
