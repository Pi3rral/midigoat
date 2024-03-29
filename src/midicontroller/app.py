try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

event_loop = asyncio.get_event_loop()

from midicontroller.esp_controller_asyncio import midi_controller
from midicontroller.controller import (
    START_WEBSERVER_COMMAND,
    START_REPL_COMMAND,
)

from .wifi import configure_network


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
            address = configure_network()
            if address is None:
                midi_controller.splash_screen("No Wifi", 3)
                continue
            midi_controller.splash_screen(address, 3)
            event_loop.create_task(webserver())
        elif command == START_REPL_COMMAND:
            print("Start REPL")
            midi_controller.splash_screen("Start REPL", 3)
            event_loop.create_task(aiorepl.task())


async def webserver():
    await web.start_server(debug=True)


async def main():
    print("Start Midi Controller")
    event_loop.create_task(midicontroller())

    print("Start Infinite Loop")
    event_loop.run_forever()
