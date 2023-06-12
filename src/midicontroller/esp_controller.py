import ujson as json
from utime import sleep_us, sleep_ms
from machine import Pin, SoftI2C
from .controller import Controller
from .bank import Bank
from lcd.esp8266_i2c_lcd import I2cLcd
from .esp32_midi import ESP32TXPort
from adafruit_midi import MIDI
from .midi import MidiPort


PULSE_WIDTH_USEC = 5
DEFAULT_CONFIG_FILE = "/controller.json"
DEFAULT_LCD_ADDRESS = 0x3F
LCD_ROWS = 4
LCD_COLS = 20

PIN_SCL = 22
PIN_SDA = 21
PIN_PL = 14
PIN_CLK = 12
PIN_DATA = 13


class ESPController(Controller):
    def __init__(self):
        # init config
        self.read_config()
        # init buttons
        self.init_buttons()
        # init pins
        self.pl_pin = Pin(PIN_PL, Pin.OUT)
        self.clk_pin = Pin(PIN_CLK, Pin.OUT)
        self.data_pin = Pin(PIN_DATA, Pin.IN)
        self.clk_pin.value(0)
        # init midi
        midi_port = ESP32TXPort(enable_tx0=False, enable_tx1=False, enable_tx2=True)
        midi = MIDI(midi_out=midi_port)
        MidiPort.midi_object = midi
        # init bank and LCD
        self.bank = Bank(
            banks_directory=self.config.get("banks_directory"),
            presets_directory=self.config.get("presets_directory"),
        )
        # WARNING! 0x27 is the breadbord address
        # actual pedal is 0x3F
        self.lcd_address = self.config.get("lcd_address", DEFAULT_LCD_ADDRESS)
        self.lcd = I2cLcd(
            SoftI2C(scl=Pin(PIN_SCL), sda=Pin(PIN_SDA)),
            self.lcd_address,
            LCD_ROWS,
            LCD_COLS,
        )
        self.print_menu()

    def read_config(self):
        try:
            with open(DEFAULT_CONFIG_FILE) as fp:
                self.config = json.load(fp)
        except Exception:
            print("Error reading config file")

    def read_buttons(self):
        self.pl_pin.value(0)
        sleep_us(PULSE_WIDTH_USEC)
        self.pl_pin.value(1)
        state_changed = False

        for i in range(0, self.nb_buttons):
            pressed = not self.data_pin.value()
            self.button_values[i] = pressed
            if self.buttons[i].compute_state(pressed):
                state_changed = True
            self.clk_pin.value(1)
            sleep_us(PULSE_WIDTH_USEC)
            self.clk_pin.value(0)
        return state_changed

    def wait_bounce(self):
        sleep_ms(200)
