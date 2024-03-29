try:
    import ujson
except:
    import json as ujson
try:
    import uos
except:
    import os as uos
import gc
from .preset import Preset

from .action import Action, BankAction

DEFAULT_BANKS_DIRECTORY = "/banks"
DEFAULT_PRESETS_DIRECTORY = "/presets"


class Bank:
    VERSION_V1 = "v1"
    VERSION_V2 = "v2"
    DEFAULT_VERSION = VERSION_V1
    NB_PHYSICAL_BUTTONS = 6
    NB_PAGES = 2

    def __init__(
        self,
        banks_directory=DEFAULT_BANKS_DIRECTORY,
        presets_directory=DEFAULT_PRESETS_DIRECTORY,
    ):
        self.is_loaded = False
        self.load_error = ""
        self.max_bank = 0
        self.banks = []
        self.current_bank = 0
        self.current_page = 0
        self.current_preset = 1
        self.presets = []
        self.presets_name = []
        self.name = None
        self.banks_directory = banks_directory
        self.presets_directory = presets_directory
        try:
            self.set_banks()
            self.load_bank()
        except Exception as e:
            pass
            # self.load_error = str(e)

    def set_banks(self):
        self.banks = sorted(uos.listdir(self.banks_directory))
        self.max_bank = len(self.banks)

    def swap_page(self):
        self.current_page = (self.current_page + 1) % self.NB_PAGES

    def bank_up(self):
        if not self.is_loaded:
            return
        self.presets = []
        gc.collect()
        self.current_bank += 1
        if self.current_bank >= self.max_bank:
            self.current_bank = 0
        self.load_bank()

    def bank_down(self):
        if not self.is_loaded:
            return
        self.presets = []
        gc.collect()
        self.current_bank -= 1
        if self.current_bank < 0:
            self.current_bank = self.max_bank - 1
        self.load_bank()

    def load_bank(self):
        bank_dir = self.banks_directory + "/" + self.banks[self.current_bank]
        with open(bank_dir + "/bank.json") as fp:
            bank_data = ujson.load(fp)
        self.name = bank_data.get("name")
        version = bank_data.get("version", self.DEFAULT_VERSION)
        if version == self.VERSION_V2:
            self.load_bank_v2_dir(bank_dir, bank_data)
        else:
            self.load_bank_v1_dir(bank_dir, bank_data)

    def load_bank_v1_dir(self, bank_dir, bank_data):
        nb_preset = len(uos.listdir(bank_dir)) - 1
        self.current_page = 0
        self.presets = []
        for i in range(0, nb_preset):
            gc.collect()
            with open(bank_dir + "/preset_" + str(i) + ".json") as fp:
                preset_data = ujson.load(fp)
            self.presets.append(
                Preset(preset_data.get("name"), preset_data.get("actions"))
            )
        for _ in range(len(self.presets), self.NB_PAGES * self.NB_PHYSICAL_BUTTONS):
            self.presets.append(Preset("NONE", []))
        self.presets_name = [preset.get_name() for preset in self.presets]
        self.is_loaded = True
        self.load_error = ""
        gc.collect()

    def load_bank_v2_dir(self, bank_dir, bank_data):
        self.current_page = 0
        self.presets = []
        bank_presets = bank_data["presets"]
        display_name = None
        for i in range(0, len(bank_presets)):
            gc.collect()
            if bank_presets[i]["type"] == "preset":
                preset_file = (
                    self.presets_directory + "/" + bank_presets[i]["name"] + ".json"
                )
                display_name = bank_presets[i].get("display_name")
            else:
                preset_file = bank_dir + "/preset_" + str(i) + ".json"
            with open(preset_file) as fp:
                preset_data = ujson.load(fp)
            self.presets.append(
                Preset(
                    display_name or preset_data.get("name"), preset_data.get("actions")
                )
            )
        for _ in range(len(self.presets), self.NB_PAGES * self.NB_PHYSICAL_BUTTONS):
            self.presets.append(Preset("NONE", []))
        self.presets_name = [preset.get_name() for preset in self.presets]
        self.is_loaded = True
        self.load_error = ""
        on_load_preset = bank_data.get("on_load_preset", None)
        if on_load_preset is not None:
            self.button_pressed(on_load_preset)
        gc.collect()

    def get_bank_info(self, bank_number):
        if bank_number <= 0 or bank_number > self.max_bank:
            raise Exception(
                "Invalid Bank Number. Must be between 1 and {}".format(self.max_bank)
            )
        bank_dir = self.banks_directory + "/" + self.banks[bank_number - 1]
        with open(bank_dir + "/bank.json") as fp:
            bank_data = ujson.load(fp)
        bank_data["nb_preset"] = len(uos.listdir(bank_dir)) - 1
        return bank_data

    def update_bank(self, bank_number, bank_data):
        bank_dir = self.banks_directory + "/" + self.banks[bank_number - 1]
        with open(bank_dir + "/bank.json", "w") as fp:
            ujson.dump(bank_data, fp)
        return "Bank {} updated".format(bank_number)

    def get_preset_info(self, preset_name):
        with open(self.presets_directory + "/" + preset_name + ".json") as fp:
            preset_data = ujson.load(fp)
        return preset_data

    def update_preset(self, preset_name, preset_data):
        with open(self.presets_directory + "/" + preset_name + ".json") as fp:
            ujson.dump(preset_data, fp)
        return "Preset {} updated".format(preset_name)

    def button_pressed(self, button_number):
        if not self.is_loaded:
            return
        self.presets[
            button_number + (self.current_page * self.NB_PHYSICAL_BUTTONS)
        ].pressed()
        self.do_bank_action()

    def button_long_pressed(self, button_number):
        if not self.is_loaded:
            return
        self.presets[
            button_number + (self.current_page * self.NB_PHYSICAL_BUTTONS)
        ].long_pressed()
        self.do_bank_action()

    def do_bank_action(self):
        bank_action = Action.get_bank_action()
        if bank_action == BankAction.NEXT:
            self.bank_up()
        elif bank_action == BankAction.PREVIOUS:
            self.bank_down()
        elif bank_action == BankAction.TOGGLE_PAGE:
            self.swap_page()
        Action.clear_bank_action()

    def get_current_bank_name(self):
        if not self.is_loaded:
            return "No Banks Loaded"
        return self.name

    def get_current_page(self):
        return self.current_page

    def get_current_presets_names(self):
        if self.current_page == 1:
            return self.presets_name[6:]
        return self.presets_name[:6]
