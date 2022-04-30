from math import floor
import random

class turing_machine:
    gate = []
    bits = []

    def __init__(self, steps=8, interval=3, prob=0.5, bit_string=None, range=32):
        #if steps == 0:
        #    raise(TypeError("Steps should be greater than 0"))
        if interval > steps:
            raise(TypeError("Interval should be less than number of steps"))
        self.bits = [0 for i in range(0, steps) if True]
        self.gate = [0 for i in range(0, steps) if True]
        if prob > 1:
            raise(TypeError("Proability not in range"))
        self.prob = proba
        self.note = None
        self.trig = False
        self.range = range
        self.set_gate(interval=interval)
        if bit_string is None:
            self.seed_bits()
        else: 
            self.set_bits(bit_string)
        # blah blah

    def set_range(self, range):
        self.range = range
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
            self.note = floor((acc / self.max) * self.range)
        else:
            self.note = None
        return(self)
    
    def get_note(self):
        return self.note



class test:
    def __init__(self, age):
        self.age = age


def move_bits(bits):
    for i in range(0,len(bits)-2):
        bits[i] = bits[i+1]
    return(bits)
