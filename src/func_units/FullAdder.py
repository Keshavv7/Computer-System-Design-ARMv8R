from amaranth import *
from amaranth.sim import *

class HalfAdder(Elaboratable):
    def __init__(self):
        self.a = Signal()  # First input
        self.b = Signal()  # Second input
        self.sum = Signal()  # Sum output
        self.carry = Signal()  # Carry output

    def elaborate(self, platform):
        m = Module()

        # Sum = a XOR b
        m.d.comb += self.sum.eq(self.a ^ self.b)

        # Carry = a AND b
        m.d.comb += self.carry.eq(self.a & self.b)

        return m

class FullAdder(Elaboratable):
    def __init__(self):
        self.a = Signal()  # First input
        self.b = Signal()  # Second input
        self.cin = Signal()  # Carry input
        self.sum = Signal()  # Sum output
        self.cout = Signal()  # Carry output

    def elaborate(self, platform):
        m = Module()

        # Intermediate signals
        half_adder1 = HalfAdder()
        half_adder2 = HalfAdder()

        m.submodules.half_adder1 = half_adder1
        m.submodules.half_adder2 = half_adder2

        # First half adder to add a and b
        m.d.comb += [
            half_adder1.a.eq(self.a),
            half_adder1.b.eq(self.b),
        ]

        # Sum from the first half adder and cin
        m.d.comb += [
            half_adder2.a.eq(half_adder1.sum),
            half_adder2.b.eq(self.cin),
        ]

        # Sum output
        m.d.comb += self.sum.eq(half_adder2.sum)

        # Carry output
        m.d.comb += self.cout.eq(half_adder1.carry | half_adder2.carry)

        return m
    
from amaranth.sim import *

def simulate_full_adder():
    full_adder = FullAdder()
    sim = Simulator(full_adder)

    def process():
        # Test cases for the full adder
        test_cases = [
            (0, 0, 0),  # a = 0, b = 0, c_in = 0
            (0, 0, 1),  # a = 0, b = 0, c_in = 1
            (0, 1, 0),  # a = 0, b = 1, c_in = 0
            (0, 1, 1),  # a = 0, b = 1, c_in = 1
            (1, 0, 0),  # a = 1, b = 0, c_in = 0
            (1, 0, 1),  # a = 1, b = 0, c_in = 1
            (1, 1, 0),  # a = 1, b = 1, c_in = 0
            (1, 1, 1),  # a = 1, b = 1, c_in = 1
        ]

        for a, b, c in test_cases:
            yield full_adder.a.eq(a)
            yield full_adder.b.eq(b)
            yield full_adder.cin.eq(c)
            yield Delay(1e-6)
            print(f"a={a}, b={b}, c={c}, sum={yield full_adder.sum}, carry={yield full_adder.cout}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_full_adder()
