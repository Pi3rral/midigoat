# Midi Controller Using Micropython on ESP32 DevKit board

## Tools

### Useful Links

https://docs.micropython.org/en/latest/esp32/quickref.html
https://www.digikey.ca/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce

### Local Virtualenv

Using pyenv-virtualenv `micropython`: `pyenv virtualenv activate micropython`

```shell
pip install -r requirements.txt
```

### External Libraries

In `libs` directory, clone the following repos:
- git@github.com:miguelgrinberg/microdot.git
- git@github.com:adafruit/Adafruit_CircuitPython_MIDI.git

They will be added to the frozen part of the custom firmware.

### Flash firmware

Erase and flash on ESP32 (option to erase at the same time is not working)
WARNING: Using more recent firmware (or custom) is not working yet

```shell
esptool.py --port /dev/tty.usbserial-0001 erase_flash
esptool.py --port /dev/tty.usbserial-0001 --chip esp32 --baud 460800 write_flash -z 0x1000 firmware/esp32-20210902-v1.20.0.bin
```

Flash only the `micropython` firmware (keep `boot` and `data`)
Example using OTA firmware in `ota_0` partition

```shell
esptool.py --port /dev/tty.usbserial-0001 --chip esp32 --baud 460800 write_flash -z 0x10000 build/GENERIC_OTA/micropython.bin
```

#### Build Firmware

Building in docker image:

```shell
docker build -f firmware/Dockerfile -t midigoat .
docker run --rm -ti --volume $PWD/firmware:/root/export midigoat /bin/bash -c "cp /micropython/ports/esp32/build-GENERIC/firmware.bin /root/export/esp32-generic-midigoat.bin"
```

Copy build directory locally
```shell
docker run --rm -ti --volume $PWD/build:/root/export midigoat /bin/bash -c "cp -R /micropython/ports/esp32/build-GENERIC_OTA /root/export/GENERIC_OTA"
```

Firmware is located in the image at `/micropython/ports/esp32/build-GENERIC/firmware.bin`

### Test live

```shell
ampy --port /dev/tty.usbserial-0001 run src/main.py
```

### Upload file

Don't forget to remove `pyc` files!

```shell
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

```shell
ampy --port /dev/tty.usbserial-0001 put src/wifi.py /wifi.py
ampy --port /dev/tty.usbserial-0001 put src/midicontroller /midicontroller
ampy --port /dev/tty.usbserial-0001 put banks_dir /banks_dir
ampy --port /dev/tty.usbserial-0001 put src/main.py /main.py
```

or from the rshell

```
rsync data/presets /pyboard/presets
mkdir /pyboard/banks
rsync data/banks_existenza/00.Generic /pyboard/banks/generic
rsync data/banks_existenza/00.Generic /pyboard/banks/generic
rsync data/banks_existenza /pyboard/banks
rsync src/midicontroller /pyboard/midicontroller
cp src/wifi.py /pyboard/
cp src/main.py /pyboard/
```

### Connect to REPL

#### Using `screen`

```shell
screen /dev/tty.usbserial-0001 115200
```
exit with `Ctrl-A; Ctrl-\`

#### Using `rshell`

```shell
rshell -p /dev/tty.usbserial-0001
```
exit with `Ctrl-D`

from `rshell`
```shell
repl
```
exit with `Ctrl-X`

#### Using `mpremote` with `aiorepl`

```
mpremote connect /dev/tty.usbserial-0001
```

Then start `aiorepl` prompt (Long press button 4)

#### Free Flash Space

From REPL

```python
import uos
fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]
fs_free = fs_stat[0] * fs_stat[3]
print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
```

## Wiring Schema

R-Tx = 10 Ohm

R-V3.3 = 47 Ohm

![diagram](img/diagram.png)

Note: Connect 74HC165 to Pin D3 (GPIO0) make the board fail to boot.

## External Libraries Used

https://github.com/adafruit/Adafruit_CircuitPython_MIDI
- added `__str__` to `MIDIMessage`, `ProgramChange` and `ControlChange` classes

https://github.com/dhylands/python_lcd


# Ideas

Long press open a setup menu:
1. Connect Home Wifi
2. Create own Wifi
3. Start/Stop Web Server
4. Start/Stop Bluetooth
5. Start REPL (AsyncIO)
6. Quit setup menu

# TODO

- Create manifest files for frozen code: https://docs.micropython.org/en/latest/reference/manifest.html#high-level-functions
- Implement OTA firmware update: 
    - https://docs.micropython.org/en/latest/library/esp32.html
    - https://github.com/orgs/micropython/discussions/9579
    - https://iot49.org/projects/internet/ota.html
- Freeze static files:
    - https://github.com/peterhinch/micropython_data_to_py
    - https://github.com/insighio/microfreezer