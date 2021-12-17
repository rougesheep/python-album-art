#!/usr/bin/env python3

import os
import configparser
import sys
import soco
import time
from requests import get
from queue import Empty
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from soco.events import event_listener

print(os.getcwd())

config = configparser.ConfigParser()

if not os.path.exists('config.ini'):
    print('Config file not found.')
    config['SONOS'] = { 'room': 'Sonos' }
    config['LED'] = { 'hardware_mapping': 'adafruit-hat-pwm', 'rows': 64, 'cols': 64, 'gpio_slowdown': 2, 'brightness': 50, 'pwm_bits': 11 }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print('Default config written to config.ini.')
    sys.exit(0)

config.read('config.ini')

options = RGBMatrixOptions()
options.rows = config['LED'].getint('rows')
options.cols = config['LED'].getint('cols')
options.hardware_mapping = config['LED']['hardware_mapping']
options.gpio_slowdown = config['LED'].getint('gpio_slowdown')
options.brightness = config['LED'].getint('brightness')
options.pwm_bits = config['LED'].getint('pwm_bits')
options.show_refresh_rate = 0

panel = RGBMatrix(options = options)

device = soco.discovery.by_name(config['SONOS']['room']).group.coordinator

print(device.player_name)

sub_transport = device.avTransport.subscribe(auto_renew=True)

while True:

    try:
        event = sub_transport.events.get(timeout=0.5)
        print(event.variables['transport_state'])
        if event.variables['transport_state'] == 'PLAYING':
            track_info = device.get_current_track_info()
            print(track_info['title'])

            image_url = track_info['album_art']

            with open('/tmp/art.jpg', 'wb') as file:
                response = get(image_url)
                file.write(response.content)

            image = Image.open('/tmp/art.jpg')

            image.thumbnail((panel.width, panel.height), Image.ANTIALIAS)

            panel.SetImage(image.convert('RGB'))
        elif event.variables['transport_state'] == 'STOPPED' or event.variables['transport_state'] == 'PAUSED_PLAYBACK':
            panel.Clear()
    except Empty:
        pass
    except KeyboardInterrupt:
        sub_transport.unsubscribe()
        event_listener.stop()
        sys.exit(0)
    time.sleep(1)
