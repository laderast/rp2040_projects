# MIDI visualizer
# Takes usb midi notes from channel 8
# And visualizes them on the 240x240 screen
# Of Pimoroni explorer.
# Simple visualizer that visualizes MIDI notes
# As part of a 144 note grid
"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""
import os
import board
import time
import terminalio
import displayio
import busio
from adafruit_display_text import label
from adafruit_display_shapes import rect
import time
import random
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from math import floor

print(usb_midi.ports)

midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0],
    in_channel=7, midi_out=usb_midi.ports[1], out_channel=0)
print("Midi test")
# Convert channel numbers at the presentation layer to the ones musicians use
print("Default output channel:", midi.out_channel + 1)
print("Listening on input channel:", midi.in_channel + 1)


# Release any resources currently in use for the displays
displayio.release_displays()


import board
import busio
import terminalio
import displayio
import digitalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=180)

button_a = digitalio.DigitalInOut(board.GP12)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.DOWN

button_b = digitalio.DigitalInOut(board.GP13)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.DOWN


# Make the display context
splash = displayio.Group()
display.show(splash)


string_msg = ""
string_val = ""

cell_height = 20
cell_width = 20
shape_list = []

note_colors = [0xff0000, 0xff8000, 0xffff00, 0x80ff00, 0x00ff00,
0x00ff80, 0x00ffff, 0x0080ff, 0x0000ff, 0x8000ff, 0xff00ff, 0xff0080]

for note in range(0, 256):
    col = note % 12
    row = floor(note / 12)
    xpos = col * cell_width
    ypos = row * cell_height
    new_rect = rect.Rect(x = xpos, y = ypos, width = cell_width,
                         height = cell_height, fill=0x0)
    splash.append(new_rect)
    shape_list.append(new_rect)

text_group1 = displayio.Group(max_size=10, scale=1, x=10, y=10)
text = "Channel: " + str(midi.in_channel)
text_area1 = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group1.append(text_area1)

splash.append(text_group1)

while True:
    msg = midi.receive()
    if button_a.value and midi_in.channel != 15:
        new_channel = midi_in.channel + 1
        midi.in_channel = new_channel
        text_area.text = "Channel: " + str(new_channel)
    if button_b.vale and midi.in_channel != 0:
        new_channel = midi_in.channel - 1
        midi.in_channel = new_channel
        text_area1.text = "Channel: " + str(new_channel)
    if msg is not None:
        if isinstance(msg, NoteOn):
            string_msg = 'NoteOn'
            # get note number
            string_val = str(msg.note)
            int_note = int(msg.note)
            shape_list[int_note].fill = note_colors[int_note % 12]
    # if a NoteOff message...
        if isinstance(msg, NoteOff):
            string_msg = 'NoteOff'
            # get note number
            string_val = str(msg.note)
            int_note = int(msg.note)
            shape_list[int_note].fill = 0x0
