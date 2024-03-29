from microdot.microdot_asyncio import Microdot, Response

try:
    from midicontroller.esp_controller_asyncio import midi_controller
except:
    from midicontroller.controller_test import midi_controller_test as midi_controller


web = Microdot()


@web.route("/")
async def index(request):
    return "Hello, world!"


@web.route("/bank_up")
async def bank_up(request):
    try:
        midi_controller.bank.bank_up()
        midi_controller.print_menu()
        return Response(status_code=200)
    except Exception as e:
        return Response(body=str(e), status_code=404)


@web.route("/bank_down")
async def bank_up(request):
    midi_controller.bank.bank_down()
    midi_controller.print_menu()
    return "Bank Down!"


@web.route("/bank/<int:bank_number>", methods=["GET"])
async def get_bank_info(request, bank_number):
    try:
        return Response(
            body=midi_controller.bank.get_bank_info(bank_number), status_code=200
        )
    except Exception as e:
        return Response(body=str(e), status_code=404)


@web.route("/bank/<int:bank_number>", methods=["POST"])
async def set_bank(request, bank_number):
    try:
        bank_data = request.json
        return Response(
            body=midi_controller.bank.update_bank(bank_number, bank_data),
            status_code=200,
        )
    except Exception as e:
        return Response(body=str(e), status_code=404)


@web.route("/preset/<string:preset_name>", methods=["GET"])
async def get_preset_info(request, preset_name):
    try:
        return Response(
            body=midi_controller.bank.get_preset_info(preset_name),
            status_code=200,
        )
    except Exception as e:
        return Response(body=str(e), status_code=404)


@web.route("/preset/<string:preset_name>", methods=["POST"])
async def set_preset(request, preset_name):
    try:
        preset_data = request.json
        return Response(
            body=midi_controller.bank.update_preset(preset_name, preset_data),
            status_code=200,
        )
    except Exception as e:
        return Response(body=str(e), status_code=404)
