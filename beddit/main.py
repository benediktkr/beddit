
from beddit.config import read_config

import bluetooth

def connect():
    config = read_config()
    mac = config['beddit']['mac']
    print(f"mac: {mac}")

    # nearby_devices = bluetooth.discover_devices(lookup_names=True)
    # for item in nearby_devices:
    #     print(item)
    #     print(dir(item))

    s = bluetooth.find_service(address=mac)
    print(s)

def cli():
    connect()
