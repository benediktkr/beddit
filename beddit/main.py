
from beddit.config import read_config

import bluetooth

def connect():
    config = read_config()
    mac = config['beddit']['mac']

    nearby_devices = bluetooth.discover_devices(lookup_names=True)

def cli():
    pass
