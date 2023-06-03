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

# RUN source tools/ci.sh && ci_esp32_idf44_setup
# build vanilla first to re-use docker layer
COPY firmware/setup.sh ${MICROPYTHON_DIR}/setup.sh
RUN ./setup.sh

# RUN source tools/ci.sh && ci_esp32_build

COPY src/midicontroller/ ${MICROPYTHON_DIR}/ports/esp32/modules/midicontroller/
COPY src/wifi.py ${MICROPYTHON_DIR}/ports/esp32/modules/wifi.py
COPY src/main.py ${MICROPYTHON_DIR}/ports/esp32/modules/boot.py
COPY firmware/inisetup.py ${MICROPYTHON_DIR}/ports/esp32/modules/inisetup.py
COPY firmware/manifest.py ${MICROPYTHON_DIR}/ports/esp32/boards/manifest_midigoat.py
COPY firmware/build.sh ${MICROPYTHON_DIR}/midigoat_build.sh

# build with custom code
# RUN source tools/ci.sh && ci_esp32_build
RUN ./midigoat_build.sh
