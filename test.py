#!/usr/bin/env python3

import sys
import soco
import time
from requests import get
from queue import Empty
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from soco.events import event_listener

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
#options.chain_length = 1
#options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 1
options.brightness = 100
options.pwm_bits = 2
options.pwm_lsb_nanoseconds = 50
options.pwm_dither_bits = 1
options.show_refresh_rate = 1

panel = RGBMatrix(options = options)

device = soco.discovery.by_name('Bedroom').group.coordinator

print(device.player_name)

track_info = device.get_current_track_info()
print(track_info['title'])

image_url = track_info['album_art']

with open('/tmp/art.jpg', 'wb') as file:
  response = get(image_url)
  file.write(response.content)

  image = Image.open('/tmp/art.jpg')

  image.thumbnail((panel.width, panel.height), Image.ANTIALIAS)

  panel.SetImage(image.convert('RGB'))


time.sleep(60)
