import network
import ujson as json
from utime import sleep_ms

NETWORK_CONFIG = "/network.json"
DEFAULT_MIDIGOAT_SSID = "MidiGoat"
DEFAULT_MIDIGOAT_PASSWORD = "midigoat"


def read_config():
    try:
        with open(NETWORK_CONFIG) as fp:
            config = json.load(fp)
    except Exception:
        config = {}
    return config


def configure_network():
    config = read_config()
    known_networks = config.get("known_networks", [])
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if len(known_networks):
        sta_if.active(True)
        for network_config in known_networks:
            sleep_ms(500)
            ssid_name = network_config.get("ssid")
            ssid_password = network_config.get("password")
            address = try_connect_wifi(sta_if, ssid_name, ssid_password)
            if address:
                ap_if.active(False)
                return address
    sta_if.active(False)
    midigoat_network = config.get("midigoat_network", {})
    if len(midigoat_network):
        midigoat_ssid = midigoat_network.get("ssid", DEFAULT_MIDIGOAT_SSID)
        midigoat_password = midigoat_network.get("password", DEFAULT_MIDIGOAT_PASSWORD)
        print(
            "Creating MidiGoat access point: {} - {}".format(
                midigoat_ssid, midigoat_password
            )
        )
        ap_if.active(True)
        ap_if.config(
            essid=midigoat_ssid,
            password=midigoat_password,
        )
        sleep_ms(5000)
        print("MidiGoat access point created")
        return True
    ap_if.active(False)
    return False


def try_connect_wifi(sta_if, ssid_name, ssid_password):
    print("Trying to connect to {}".format(ssid_name))
    sta_if.connect(ssid_name, ssid_password)
    for _ in range(0, 15):
        print(".")
        sleep_ms(1000)
        if sta_if.isconnected():
            print("Connected to {}".format(sta_if.ifconfig()[0]))
            address = "IP: {}".format(sta_if.ifconfig()[0])
            return address
    return None
