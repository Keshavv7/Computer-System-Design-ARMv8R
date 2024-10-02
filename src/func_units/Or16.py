from amaranth import *
from amaranth.sim import *


class Or8(Elaboratable):
    def __init__(self):
        self.a = Signal(8)   # 8-bit input a
        self.b = Signal(8)   # 8-bit input b
        self.out = Signal(8) # 8-bit output

    def elaborate(self, platform):
        m = Module()

        # Bitwise OR operation between a and b
        m.d.comb += self.out.eq(self.a | self.b)

        return m

class Or16(Elaboratable):
    def __init__(self):
        self.a = Signal(16)  # 16-bit input a
        self.b = Signal(16)  # 16-bit input b
        self.out = Signal(16) # 16-bit output

    def elaborate(self, platform):
        m = Module()

        # Instantiate two 8-bit OR gates
        or8a = Or8()
        or8b = Or8()
        m.submodules.or8a = or8a
        m.submodules.or8b = or8b

        # Connect the lower 8 bits to or8a
        m.d.comb += [
            or8a.a.eq(self.a[:8]),
            or8a.b.eq(self.b[:8]),
            self.out[:8].eq(or8a.out)
        ]

        # Connect the upper 8 bits to or8b
        m.d.comb += [
            or8b.a.eq(self.a[8:]),
            or8b.b.eq(self.b[8:]),
            self.out[8:].eq(or8b.out)
        ]

        return m


def simulate_or16():
    or16 = Or16()
    sim = Simulator(or16)

    def process():
        # Test case 1: a = 0000000000000000, b = 0000000000000000
        yield or16.a.eq(0b0000000000000000)
        yield or16.b.eq(0b0000000000000000)
        yield Delay(1e-6)
        print(f"a=0000000000000000, b=0000000000000000, out={bin((yield or16.out))[2:].zfill(16)}")

        # Test case 2: a = 0000000000000000, b = 1111111111111111
        yield or16.a.eq(0b0000000000000000)
        yield or16.b.eq(0b1111111111111111)
        yield Delay(1e-6)
        print(f"a=0000000000000000, b=1111111111111111, out={bin((yield or16.out))[2:].zfill(16)}")

        # Test case 3: a = 1111111111111111, b = 1111111111111111
        yield or16.a.eq(0b1111111111111111)
        yield or16.b.eq(0b1111111111111111)
        yield Delay(1e-6)
        print(f"a=1111111111111111, b=1111111111111111, out={bin((yield or16.out))[2:].zfill(16)}")

        # Test case 4: a = 1010101010101010, b = 0101010101010101
        yield or16.a.eq(0b1010101010101010)
        yield or16.b.eq(0b0101010101010101)
        yield Delay(1e-6)
        print(f"a=1010101010101010, b=0101010101010101, out={bin((yield or16.out))[2:].zfill(16)}")

        # Test case 5: a = 0011110011000011, b = 0000111111110000
        yield or16.a.eq(0b0011110011000011)
        yield or16.b.eq(0b0000111111110000)
        yield Delay(1e-6)
        print(f"a=0011110011000011, b=0000111111110000, out={bin((yield or16.out))[2:].zfill(16)}")

        # Test case 6: a = 0001001000110100, b = 1001100001110110
        yield or16.a.eq(0b0001001000110100)
        yield or16.b.eq(0b1001100001110110)
        yield Delay(1e-6)
        print(f"a=0001001000110100, b=1001100001110110, out={bin((yield or16.out))[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_or16()
