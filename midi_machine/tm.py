from math import floor
import random

class turing_machine:
    gate = []
    bits = []
    range = 2

    def __init__(self, steps, interval, prob):
        #if steps == 0:
        #    raise(TypeError("Steps should be greater than 0"))
        if interval > steps:
            raise(TypeError("Interval should be less than number of steps"))
        self.bits = [0 for i in range(0, steps) if True]
        self.gate = [0 for i in range(0, steps) if True]
        if prob > 1:
            raise(TypeError("Proability not in range"))
        self.prob = prob
        self.note = None
        self.trig = False
        self.set_gate(interval=interval)
        #return(None)


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
        bit_string.split()

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
        for i in range(0, len(self.bits)-2):
            self.bits[i] = self.bits[i+1]
            acc = (acc * 2) + self.bits[i]
            self.max = (self.max * 2) + 1
            print(i)
            if self.bits[i] != 0 and self.gate[i] != 0:
                self.trig = True

        print(self.trig)        
        flip = random.random()
        flip_inv = 1 - flip
        if self.prob >= flip:
            self.bits[len(self.bits)-1] = feedback
        else:
            self.bits[len(self.bits)-1] = random.randint(0,1)     
        if self.trig:
            self.note = (acc / self.max * self.range)
        else:
            self.note = None
        return(self)
    
    def get_note(self):
        return self.note


class test:
    def __init__(self, age):
        self.age = age
