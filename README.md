# Sonos Album Art

This is a simple Python script that displays album art from a Sonos system for the [Adafruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211).

## Running

The first run will generate a default config file for you. Check this and make sure it matches your setup. Most of the options come from the [rpi-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) and they're explained much better than I could over there. You will need to set your Sonos room name.

To run in the foreground:

```
sudo ./album-art.py
```

## Adding as a systemd service

To use this as a systemd service, copy the unit files in the `systemd` folder to your systemd directory, usually `/etc/systemd/system`, reload and start the services.

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
