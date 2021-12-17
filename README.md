# Sonos Album Art

This is a simple Python script that displays album art from a Sonos system for the [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211) on a Raspberry Pi.

![Album art display](album.png)

## Hardware

From my testing, you need a Raspberry Pi 3B or newer to run this on a 64x64 panel. A Pi 2 or Zero 2 are not powerful enough and you will get flicker on the matrix. There is also something weird going on with the newest Raspberry Pi OS kernel and I had to use the legacy image instead to get a stable picture displayed.

## Installation

* Clone this repo to `/opt` on your Raspberry Pi
* Install the led libary for Python3
  * Follow the instructions [here](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)
* Install requirements
```
sudo apt install python3 python3-pip python3-pillow
sudo pip install soco
```

## Running

The first run will generate a default config file for you. Check this and make sure it matches your setup. Most of the options come from the [rpi-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) and they're explained much better than I could over there. You will need to set your Sonos room name.

To run in the foreground:

```
sudo ./album-art.py
```

## Adding as a systemd service

To use this as a systemd service, copy the unit files in the `systemd` folder to your systemd directory, usually `/etc/systemd/system`, reload and start the services.

These files have absolute paths in them and expect you to have cloned the repo into `/opt`

```
sudo cp systemd/* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now python-album-art
```

There is also a pair of watcher files that restart the main service if main file or config changes. You can enable this in the same way.

```
sudo systemctl enable --now python-album-art-watcher.path
```

## Libraries

* [SoCo](https://github.com/SoCo/SoCo) - Python library for controlling Sonos devices
* [rpi-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) - LED matrix controller with Python bindings
