# beddit

## BLE

Reverse engineering the BLE protocol: https://medium.com/inmoodforlife/beddit-reverse-engineering-c4bdca8e07b8

 The code in the repo this repo was forked from is for an older version of the Beddit that uses RFCOMM serial over Bluetooth. Mine probably doesnt use RFCOMM, as it seems to use BLE.

## dependencies

```shell
apt-get install libbluetooth-dev
```

## connect

```shell
$ bluetoothctl power on
$ bluetoothctl piarable on
$ bluetoothctl pair ${beddit_mac}
$ bluetoothctl trust ${beddit_mac}

$ bluetoothctl connect ${beddit_mac}
Attempting to connect to EA:26:7D:4A:ED:E4
[CHG] Device EA:26:7D:4A:ED:E4 Connected: yes
[CHG] Device EA:26:7D:4A:ED:E4 Connected: no
Connection successful
[CHG] Device EA:26:7D:4A:ED:E4 Connected: yes
[CHG] Device EA:26:7D:4A:ED:E4 Connected: no
[CHG] Device EA:26:7D:4A:ED:E4 Paired: yes

$ bluetoothctl devices
Device EA:26:7D:4A:ED:E4 Beddit 2564
$ bluetoothctl paired-devices
Device EA:26:7D:4A:ED:E4 Beddit 2564

$ bluetoothctl info ${beddit_mac}
Device EA:26:7D:4A:ED:E4 (random)
        Name: Beddit 2564
        Alias: Beddit 2564
        Appearance: 0x03c0
        Paired: yes
        Trusted: yes
        Blocked: no
        Connected: no
        LegacyPairing: no
        UUID: Generic Access Profile    (00001800-0000-1000-8000-00805f9b34fb)
        UUID: Generic Attribute Profile (00001801-0000-1000-8000-00805f9b34fb)
        UUID: Device Information        (0000180a-0000-1000-8000-00805f9b34fb)
        UUID: Environmental Sensing     (0000181a-0000-1000-8000-00805f9b34fb)
        UUID: Vendor specific           (e6807d20-b90a-11e5-a837-0800200c9a66)



$ bluetoothctl agent on

```

maybe `bluetooth.service` needs to be running, or is the agent?

# beddit-python-bt
Python library for reading raw data from Beddit Bluetooth 2 device

## Specifications for Bluetooth 2 sensor protocol

The sensor has two states: Command and Streaming. Both states have a few
commands for performing appropriate tasks. The commands are plain text in
capital letters and end with `\n` or `\r\n`. If a command is mistyped the
device will respond with an error message.

When a new connection is opened the device is initially in Command mode.
If the connection unexpectedly breaks the device will enter Command mode.

Command mode commands:

* OK  -  Test that the device can communicate. The device responds OK, and a
  newline.

* INFO  -  Get device info. The info is a key-value mapping in a textual format
  which can be easily parsed. The info ends with a newline.

* START [n]  -  Enter the streaming mode. The parameter n is a streaming timeout
  in seconds. When enabled a CONT command must be sent within the timeout,
  otherwise the device will return to Command mode. So for instance if "START 5"
  is given, a CONT command must be issued at least every 5 seconds. If the
  parameter is omitted the CONT command does not need to be used.


Streaming mode commands:

* STOP  -  Enter command mode.

* CONT  -  Confirmation to continue sending data. If a streaming timeout is
  given with the START command, the CONT command must be issued within the
  timeout. If the streaming timeout is not set this command has no effect.


While in Streaming mode the device will continuously send packets with the
following format:

```
Field  : Description

uint32 : Packet number, starting from 0, with increments of one. In python you
         can read this for instance like this:
         packet_number = struct.unpack('<I', data[0:4])

uint16 : payload length in number of bytes payload data

crc32  : 4 byte wide crc checksum. The checksum includes the bytes of the three
         above fields. For instance libz can be used for crc calculation, or the
         Python equivalent: crc = binascii.crc32(data) & 0xffffffff

Payload data : As many channels in interlaced PCM as specified by the INFO
               response, in uint16 format.
```

All numbers are in little endian byte order. Packets are sent as a stream, one
after another with no additional boundary bytes. The payload data is the raw
sample data, so you can form a signal just by concatenating the payload data of
consecutive packets. The samples are of type uint16.
