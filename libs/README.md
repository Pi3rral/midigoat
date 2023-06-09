# External Libraries

They will be added to the frozen part of the custom firmware.

## Adafruit MIDI

Clone Adafruit_CircuitPython_MIDI as is
- git@github.com:adafruit/Adafruit_CircuitPython_MIDI.git

## Microdot

Warning: Needs modification!

Clone Microdot in a separate repo `git clone git@github.com:miguelgrinberg/microdot.git microdot_git`

Then copy `microdot.py` and `microdot_asyncio.py` in a new directory `microdot`
Then change imports in `microdot_asyncio.py` for relative imports
- `from microdot import ...` -> `from .microdot import ...`

## LCD API

Download the following into `lcd`
- `lcd_api.py` and `esp8266_i2c_lcd.py` from `https://github.com/dhylands/python_lcd`
