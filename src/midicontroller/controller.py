from time import sleep, ticks_ms, ticks_diff
from .bank import Bank


FS3X_TIP_IDX = 7
FS3X_RING_IDX = 6

NO_COMMAND = 0
START_WEBSERVER_COMMAND = 1
START_REPL_COMMAND = 2


class Button:
    LONG_PRESS_MS = 1000
    LONG_PRESS_REPEAT_MS = 700

    INTERNAL_STATE_ON = 1
    INTERNAL_STATE_OFF = 0

    STATE_OFF = 0
    STATE_PRESSED = 1
    STATE_LONG_PRESSED = 2
    STATE_RELEASED = 3

    def __init__(self):
        self.state = self.STATE_OFF
        self.state_changed = False
        self.ticks_start = None

    def compute_state(self, current_internal_state):
        """Compute button state
        return bool if state has changed
        """
        if current_internal_state == self.INTERNAL_STATE_ON:
            if self.state == self.STATE_OFF:
                self.state = self.STATE_PRESSED
                self.ticks_start = ticks_ms()
                return True
            elif (
                self.state == self.STATE_PRESSED
                and ticks_diff(ticks_ms(), self.ticks_start) > self.LONG_PRESS_MS
            ):
                self.state = self.STATE_LONG_PRESSED
                self.ticks_start = ticks_ms()
                return True
            elif (
                self.state == self.STATE_LONG_PRESSED
                and ticks_diff(ticks_ms(), self.ticks_start) > self.LONG_PRESS_REPEAT_MS
            ):
                self.ticks_start = ticks_ms()
                return True
        elif self.state != self.STATE_OFF:
            self.state = self.STATE_OFF
            return True
        return False


class Controller:
    bank = None
    lcd = None
    button_values = []
    nb_buttons = 8
    buttons = []

    def __init__(self):
        self.bank = Bank()
        self.init_buttons()

    def init_buttons(self):
        for _ in range(self.nb_buttons):
            self.button_values.append(0)
            self.buttons.append(Button())

    def read_buttons(self):
        return False

    def wait_bounce(self):
        pass

    def wait(self, seconds):
        sleep(seconds)

    def print_menu(self):
        if not self.lcd:
            return
        if not self.bank.is_loaded:
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr("Error Loading Bank " + str(self.bank.current_bank))
            self.lcd.move_to(0, 1)
            self.lcd.putstr(self.bank.load_error)
            return

        patch_names = self.bank.get_current_presets_names()
        self.lcd.clear()
        self.lcd.move_to(0, 3)
        self.lcd.putstr(patch_names[0])
        offset = int((6 - len(patch_names[1])) / 2)
        self.lcd.move_to(7 + max(offset, 0), 3)
        self.lcd.putstr(patch_names[1])
        self.lcd.move_to(20 - len(patch_names[2]), 3)
        self.lcd.putstr(patch_names[2])
        self.lcd.move_to(0, 1)
        self.lcd.putstr("Bank: " + self.bank.get_current_bank_name())
        self.lcd.move_to(0, 2)
        self.lcd.putstr("Page: " + str(self.bank.get_current_page()))
        self.lcd.move_to(0, 0)
        self.lcd.putstr(patch_names[3])
        offset = int((6 - len(patch_names[4])) / 2)
        self.lcd.move_to(7 + max(offset, 0), 0)
        self.lcd.putstr(patch_names[4])
        self.lcd.move_to(20 - len(patch_names[5]), 0)
        self.lcd.putstr(patch_names[5])

    def splash_screen(self, message, seconds):
        if not self.lcd:
            return
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(message)
        sleep(seconds)
        self.print_menu()

    def loop(self):
        command = NO_COMMAND
        if self.read_buttons():
            if self.buttons[FS3X_TIP_IDX].state == Button.STATE_PRESSED:
                if self.buttons[FS3X_RING_IDX].state == Button.STATE_PRESSED:
                    self.bank.bank_up()
                else:
                    self.bank.swap_page()
            elif self.buttons[FS3X_RING_IDX].state == Button.STATE_PRESSED:
                self.bank.bank_down()
            elif self.buttons[0].state == Button.STATE_LONG_PRESSED:
                self.bank.bank_down()
            elif self.buttons[2].state == Button.STATE_LONG_PRESSED:
                self.bank.bank_up()
            elif self.buttons[3].state == Button.STATE_LONG_PRESSED:
                command = START_REPL_COMMAND
            elif self.buttons[5].state == Button.STATE_LONG_PRESSED:
                command = START_WEBSERVER_COMMAND
            else:
                for i in range(0, 6):
                    if self.buttons[i].state == Button.STATE_PRESSED:
                        self.bank.button_pressed(i)
                    elif self.buttons[i].state == Button.STATE_LONG_PRESSED:
                        self.bank.button_long_pressed(i)
            self.wait_bounce()
            self.print_menu()
        return command

    def bank_up(self):
        self.bank.bank_up()

    def bank_down(self):
        self.bank.bank_down()

    def main(self):
        while True:
            self.loop()
