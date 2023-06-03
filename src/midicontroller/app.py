try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from midicontroller.esp_controller_asyncio import midi_controller
from midicontroller.controller import (
    START_WEBSERVER_COMMAND,
    START_REPL_COMMAND,
)

import wifi

from midicontroller.webserver import web

try:
    import aiorepl
except ImportError:
    pass


async def midicontroller():
    while True:
        command = midi_controller.loop()
        await asyncio.sleep(0.005)
        if command == START_WEBSERVER_COMMAND:
            print("Start Web Server")
            midi_controller.splash_screen("Start Web Server", 1)
            address = wifi.connect_home_wifi()
            midi_controller.splash_screen(address, 3)
            asyncio.create_task(webserver())
        elif command == START_REPL_COMMAND:
            print("Start REPL")
            asyncio.create_task(aiorepl.task())


async def webserver():
    await web.start_server(debug=True)


async def main():
    print("Start Midi Controller")
    asyncio.create_task(midicontroller())

    # Start webserver at start if any button is pressed
    # if midi_controller.is_button_pressed():
    #     print("Start Web Server")
    #     midi_controller.splash_screen("Start Web Server", 1)
    #     address = wifi.connect_home_wifi()
    #     midi_controller.splash_screen(address, 3)
    #     asyncio.create_task(webserver())
    # else:
    #     midi_controller.splash_screen("No Web Server", 1)
    #     print("No Web Server")

    print("Start Infinite Loop")
    while True:
        await asyncio.sleep(10)
