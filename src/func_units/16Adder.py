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

class Adder16(Elaboratable):
    def __init__(self):
        self.a = Signal(16)  # 16-bit input a
        self.b = Signal(16)  # 16-bit input b
        self.cin = Signal()   # Carry input
        self.sum = Signal(16) # 16-bit sum output
        self.cout = Signal()  # Carry output

    def elaborate(self, platform):
        m = Module()

        # Create a chain of full adders
        carry = self.cin
        for i in range(16):
            full_adder = FullAdder()
            m.submodules[f"full_adder_{i}"] = full_adder
            
            # Connect inputs
            m.d.comb += [
                full_adder.a.eq(self.a[i]),
                full_adder.b.eq(self.b[i]),
                full_adder.cin.eq(carry),
                self.sum[i].eq(full_adder.sum),
            ]

            # Connect carry output
            carry = full_adder.cout

        # Final carry out
        m.d.comb += self.cout.eq(carry)

        return m
    

def simulate_add16():
    add16 = Adder16()
    sim = Simulator(add16)

    def process():
        # Test cases for the 16-bit adder
        test_cases = [
            (0b0000000000000000, 0b0000000000000000),  # a = 0, b = 0
            (0b0000000000000000, 0b1111111111111111),  # a = 0, b = 65535
            (0b1111111111111111, 0b1111111111111111),  # a = 65535, b = 65535
            (0b1010101010101010, 0b0101010101010101),  # a = 43690, b = 21845
            (0b0011110011000011, 0b0000111111110000),  # a = 15315, b = 40320
            (0b0001001000110100, 0b1001100001110110),  # a = 37332, b = 39186
        ]

        for a, b in test_cases:
            yield add16.a.eq(a)
            yield add16.b.eq(b)
            yield Delay(1e-6)
            out = yield add16.sum
            print(f"a={bin(a)[2:].zfill(16)}, b={bin(b)[2:].zfill(16)}, sum={bin(out)[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_add16()
