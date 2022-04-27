class turing_machine:
    bits = []
    gate = []
    range = 2
    def __init__(self, steps=8, interval = 3, prob=0.5):
        self.bits = [0 for i in range(0, steps) if True]
        self.gate = [0 for i in range(0, steps) if True]
        self.prob = prob
        self.note = None
        self.trig = False
        self.set_gate(interval=interval)
        return(self)
    def set_prob(self, prob):
        self.prob = prob
        return(self)
    def set_gate(self, interval=3):
        if interval >= len(self.gate):
            interval = floor(interval / 2)
        self.gate = [1 if i % interval == 0 else 0 for i in range(0,len(self.gate))]
        self.gate[len(self.gate)-1] = 0
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
        self.bits = self.bits.pop()
        for i in range(0, len(self.bits)-2):
            acc = (acc * 2) + bits[i]
            self.max = (self.max * 2) + 1
            if self.bits[i] <> 0 and self.gate[i] <> 0:
                trig = True
        flip = random()
        flip_inv = 1 - flip
        if self.prob >= flip:
            self.bits.append(int(feedback))
        else:
            self.bits.append(randint(0,1))
        if self.trig:
            self.note = (self.acc / self.max * self.range)
        else:
            self.note = None
        return(self)
