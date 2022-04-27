# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""I2C rotary encoder NeoPixel color picker and brightness setting example."""
from bisect import bisect
from pickle import BINBYTES
import board
import time
from rainbowio import colorwheel
import terminalio
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
from random import randint
import neopixel as neop
import board
import busio
import digitalio as digio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()
oled_reset = board.D9
# Use for I2C for STEMMA OLED
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D, reset=oled_reset)

#  STEMMA OLED dimensions. can have height of 64, but 32 makes text larger
WIDTH = 128
HEIGHT = 64
BORDER = 0

#  setup for STEMMA OLED
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

tempo = 60
orig_tempo = tempo
divide = 120 / tempo
prev_position = 0


# create the displayio object
splash = displayio.Group()
display.show(splash)


menu_text = "Menu: bpm" 
menu_text_area = label.Label(
    terminalio.FONT, text=menu_text, color=0xFFFFFF, x=4, y=6
)
splash.append(menu_text_area)

menu_rect = Rect(0, 0, 64, 16, fill=None, outline=0xFFFFFF)
splash.append(menu_rect)

#  text for BPM
bpm_text = "BPM: %d" % orig_tempo
bpm_text_area = label.Label(
    terminalio.FONT, text=bpm_text, color=0xFFFFFF, x=4, y=22
)
splash.append(bpm_text_area)

bpm_rect = Rect(0, 16, 64, 16, fill=None, outline=0xFFFFFF)
splash.append(bpm_rect)

step_text = "Steps: 16"
step_text_area = label.Label(terminalio.FONT, text=step_text, color=0xFFFFFF, x=66, y=22)
splash.append(step_text_area)

step_rect = Rect(64, 16, 64, 16, fill=None,outline = 0xFFFFFF)
splash.append(step_rect)

#  text for key
key_text = "Key: C"
key_text_area = label.Label(
    terminalio.FONT, text=key_text, color=0xFFFFFF, x=4, y=36
)
splash.append(key_text_area)

key_rect = Rect(0, 30, 50, 16, fill=None, outline=0xFFFFFF)
splash.append(key_rect)

#  text for mode
prob_text = "Prob: 0.5"
prob_text_area = label.Label(
    terminalio.FONT, text=prob_text, color=0xFFFFFF, x=54, y=36
)
splash.append(prob_text_area)

mode_rect = Rect(50, 30, 78, 16, fill=None, outline=0xFFFFFF)
splash.append(mode_rect)



# midi setup
#uart = busio.UART(board.TX, board.RX, baudrate=31250)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=5)
midi2 = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=7)

#midi = adafruit_midi.MIDI(midi_out=uart, out_channel=5)
#midi2 = adafruit_midi.MIDI(midi_out=uart, out_channel=7)
#  arrays of notes in each key
aminor_pent = [57, 57, 60, 62, 64, 67, 67, 69, 69]
key_of_C = [60, 62, 64, 65, 67, 69, 71, 72, 74]
key_of_Csharp = [61, 63, 65, 66, 68, 70, 72, 73]
key_of_D = [62, 64, 66, 67, 69, 71, 73, 74]
key_of_Dsharp = [63, 65, 67, 68, 70, 72, 74, 75]
key_of_E = [64, 66, 68, 69, 71, 73, 75, 76]
key_of_F = [65, 67, 69, 70, 72, 74, 76, 77]
key_of_Fsharp = [66, 68, 70, 71, 73, 75, 77, 78]
key_of_G = [67, 69, 71, 72, 74, 76, 78, 79]
key_of_Gsharp = [68, 70, 72, 73, 75, 77, 79, 80]
key_of_A = [69, 71, 73, 74, 76, 78, 80, 81]
key_of_Asharp = [70, 72, 74, 75, 77, 79, 81, 82]
key_of_B = [71, 73, 75, 76, 78, 80, 82, 83]

#  array of keys
keys = [key_of_C, key_of_Csharp, key_of_D, key_of_Dsharp, key_of_E, key_of_F, key_of_Fsharp,
        key_of_G, key_of_Gsharp, key_of_A, key_of_Asharp, key_of_B]

#  array of note indexes for modes
fifths = [0, 4, 3, 7, 2, 6, 4, 7]
major = [4, 2, 0, 3, 5, 7, 6, 4]
minor = [5, 7, 2, 4, 6, 5, 1, 3]
pedal = [5, 5, 5, 6, 5, 5, 5, 7]

#  defining variables for key name strings
C_name = "C"
Csharp_name = "C#"
D_name = "D"
Dsharp_name = "D#"
E_name = "E"
F_name = "F"
Fsharp_name = "F#"
G_name = "G"
Gsharp_name = "G#"
A_name = "A"
Asharp_name = "A#"
B_name = "B"

#  array of strings for key names for use with the display
key_names = [C_name, Csharp_name, D_name, Dsharp_name, E_name, F_name, Fsharp_name,
             G_name, Gsharp_name, A_name, Asharp_name, B_name]

menu_list = ["bpm", "key", "steps", "prob", "scale"]

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

seesaw = seesaw.Seesaw(board.I2C(), 0x36)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
switch = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.5

led = neop.NeoPixel(board.NEOPIXEL, 1)

last_position = -1
color = 0  # start at red

previous_note = 60
previous_note2 = 60
time_click = 0

scale_degree = 0
scale_degree2 = 0
octave = 0

key_pos = 0
orig_key_pos = 0
previous_key_pos = 0
previous_step_pos = 16
previous_prob_pos = 0.5
previous_tempo = 60
run = 0
run_state = False
menu_pos = 0

bits = [0 for i in range(0, previous_step_pos) if True]
gate = [0 for i in range(0, previous_step_pos) if True]


settings = {
    "bpm": previous_tempo,
    "key" : key_names[previous_key_pos],
    "prob" : previous_prob_pos,
    "steps" : previous_step_pos,
    "bits" : bits,
    "gate" : gate
}

menu_item = "bpm"


while True:

    if switch.value is not True:
        menu_pos = menu_pos + 1
        menu_pos = menu_pos % len(menu_list)
        menu_item = menu_list[menu_pos]
        menu_text_area.text = "Menu: " + menu_item

    position = -encoder.position

    if menu_item == "bpm":
        #encoder.set_encoder_position(0)
        diff = position - prev_position
        if abs(diff) > 0:
            tempo = diff + previous_tempo
            #print(tempo)
            bpm_text_area.text = "BPM:%d" % tempo
            #  updates calculations for beat division
            sixteenth = 15 / tempo
            eighth = 30 / tempo
            quarter = 60 / tempo
            half = 120 / tempo
            whole = 240 / tempo
            #  updates array of beat divisions
            beat_division = [whole, half, quarter, eighth, sixteenth]
            #  updates display
            bpm_text_area.text = "BPM:%d" % tempo
            settings["bpm"] = tempo
            time.sleep(0.001)
            divide = half
            previous_tempo = tempo

    if menu_item == "steps":
        diff = position - prev_position
        if abs(diff) > 0:
            step_pos = (previous_step_pos + diff) % 16
            time.sleep(0.001)
            previous_step_pos = step_pos
            settings["steps"] = step_pos
            step_text_area.text = "Steps: %d" % step_pos

    if menu_item == "key":
        #encoder = set_encoder_position(0)
        diff = position - prev_position
        if abs(diff) > 0:
            key_pos = (previous_key_pos + diff) % len(key_names)
            key_n = key_names[key_pos]
            settings["key"] = key_pos
            key_text_area.text = "Key: " + key_n
            time.sleep(0.001)
            previous_key_pos = key_pos             

    if menu_item == "prob":
        diff = position - prev_position
        if abs(diff) > 0:
            prob_pos = previous_prob_pos + (diff * 0.02)
            time.sleep(0.001)
            settings["prob"] = prob_pos
            prob_text_area.text = "Prob: " + str(prob_pos)
            previous_prob_pos = prob_pos

    prev_position = position

    if switch.value:
        run_state = True
        # negate the position to make clockwise rotation positive
        
        #scale_degree2 = min(scale_degree + randint(0,3), 7)
        #note2 = aminor_pent[scale_degree2] + (octave - 1) * 12

        if (time.monotonic() - run) >= divide:
            time_click = time_click + 1
            led.fill(0x555555)
            run = time.monotonic()
            coin1 = randint(0,2)
            coin2 = randint(0,2)
            #print(time_click)
            if time_click % 3 == 0 and coin1 == 0:
                pixel.fill(0x550000)
                scale_degree = randint(0,8)
                current_note = aminor_pent[scale_degree]
                octave = randint(-1,2)
                current_note = current_note + (octave * 12)
                midi.send(NoteOff(previous_note))
                midi.send(NoteOn(current_note))
                print(current_note)
                previous_note = current_note
                time.sleep(0.001)
            if time_click % 4 == 0 and coin2 == 0:
                pixel.fill(0x005500)
                scale_degree2 = min(scale_degree + randint(0,3), 7)
                note2 = aminor_pent[scale_degree2] + (octave - 1) * 12
                midi2.send(NoteOff(previous_note2))
                midi2.send(NoteOn(note2))
                previous_note2 = note2
                print(note2)
                time.sleep(0.001)
    if not switch.value:
        if run_state:
            all_note_off = ControlChange(123, 0)
            #  CC message is sent
            midi.send(all_note_off)
            midi2.send(all_note_off)
            run_state = False
            time.sleep(0.001)


    #print("current_note: " + str(current_note))
    pixel.fill(0x000000)
    led.fill(0x000000)
    if position != last_position:
        print(position)

        if switch.value:
            # Change the LED color.
            if position > last_position:  # Advance forward through the colorwheel.
                color += 1
            else:
                color -= 1  # Advance backward through the colorwheel.
            color = (color + 256) % 256  # wrap around to 0-256
            pixel.fill(colorwheel(color))

        else:  # If the button is pressed...
            # ...change the brightness.
            if position > last_position:  # Increase the brightness.
                pixel.brightness = min(1.0, pixel.brightness + 0.1)
            else:  # Decrease the brightness.
                pixel.brightness = max(0, pixel.brightness - 0.1)


    last_position = position
    #previous_note = current_note
    #previous_note2 = note2
    interval = .01
    time.sleep(interval)

