from array import array
from math import floor
from math import isnan
import random

class tmi:
    bits = []
    gate = []

    def __init__(self, step=8, interval=3, prob=0.5, bit_string=None, range_note=32):
        #if steps == 0:
        #    raise(TypeError("Steps should be greater than 0"))
        if interval > step:
            raise(TypeError("Interval should be less than number of steps"))
        steps = int(step)
        self.bits = [0 for j in range(int(step))]
        self.gate = [0 for j in range(step)]
        if prob > 1:
            raise(TypeError("Probability not in range"))
        self.prob = prob
        self.note = None
        self.trig = False
        self.range_note = range_note
        self.interval = interval
        self.set_gate(interval=interval)
        if bit_string is None:
            self.seed_bits()
        else: 
            self.set_bits(bit_string)
        # blah blah

    def set_range(self, range_note):
        self.range_notes = range_note
        return(self)

    def set_prob(self, prob):
        self.prob = prob
        return(self)

    def seed_bits(self):
        self.bits = [1 if random.random() > self.prob else 0 for i in range(0,len(self.bits))]

    def set_gate(self, interval=3):
        if interval >= len(self.gate):
            interval = interval - 2
        self.gate = [1 if i % interval == 0 else 0 for i in range(0,len(self.gate))]
        self.gate[len(self.gate)-1] = 0
        return(self)

    def set_bits(self, bit_string):
        self.bits = [int(i) for i in bit_string]
        return(self)
    
    def set_bit_length(self, steps):
        bit_string = self.get_bits()
        diff = len(bit_string) - steps
        diff = min(16, diff)
        if diff > 0:
            pad_string = "0" * diff
            self.set_bits(bit_string + pad_string)
        if diff < 0:
            new_bits = bit_string[0:steps]
            self.set_bits(new_bits)
        return(self)

    def get_bits(self):
        bit_string = "".join([str(n) for n in self.bits])
        return(bit_string)

    def get_gates(self):
        bit_string = "".join([str(n) for n in self.gate])
        return(bit_string)
    
    def tick(self):
        self.max = 1
        feedback = self.bits[0]
        acc = feedback
        self.trig = False 
        for i in range(len(self.bits)-1):
            self.bits[i] = self.bits[i+1]
            acc = (acc * 2) + self.bits[i]
            self.max = (self.max * 2) + 1
            if self.bits[i] != 0 and self.gate[i] != 0:
                self.trig = True

        flip = random.random()
        flip_inv = 1 - flip
        if flip >= self.prob:
            self.bits[len(self.bits)-1] = feedback
        else:
            self.bits[len(self.bits)-1] = random.randint(0,1)     
        if self.trig:
            if not isnan(acc / self.max):
                self.note = floor((acc / self.max) * self.range_note)
        else:
            self.note = None
        return(self)
    
    def get_note(self):
        return self.note



class test:
    def __init__(self, age):
        self.age = age


def scale_expand(scale):
    out_list = [[(scale[e] + 12 * i) for e in range(len(scale))] for i in range(0,10)]
    flat_list = [item for sublist in out_list for item in sublist]
    return(flat_list)


def quantize_to_scale(note, scale):
    full_scale = scale_expand(scale)
    dist = [abs(note - e) for e in scale]
    out_note = scale[min(range(len(scale)), key = lambda i: abs(scale[i]-note))]
    return(out_note)