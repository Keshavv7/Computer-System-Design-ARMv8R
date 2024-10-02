from amaranth import *
from amaranth.sim import *

class Not8(Elaboratable):
    def __init__(self):
        self.in_ = Signal(8)   # 8-bit input
        self.out = Signal(8)   # 8-bit output

    def elaborate(self, platform):
        m = Module()

        # Invert each bit of the input to produce the output
        for i in range(8):
            m.d.comb += self.out[i].eq(~self.in_[i])

        return m

class Not16(Elaboratable):
    def __init__(self):
        self.in_ = Signal(16)  # 16-bit input
        self.out = Signal(16)  # 16-bit output

    def elaborate(self, platform):
        m = Module()

        # Instantiate two 8-bit NOT gates
        not8a = Not8()
        not8b = Not8()
        m.submodules.not8a = not8a
        m.submodules.not8b = not8b

        # Connect the lower 8 bits to not8a
        m.d.comb += [
            not8a.in_.eq(self.in_[:8]),
            self.out[:8].eq(not8a.out)
        ]

        # Connect the upper 8 bits to not8b
        m.d.comb += [
            not8b.in_.eq(self.in_[8:]),
            self.out[8:].eq(not8b.out)
        ]

        return m



def simulate_not16():
    not16 = Not16()
    sim = Simulator(not16)

    def process():
        # Test case 1: input = 0000000000000000
        yield not16.in_.eq(0b0000000000000000)
        yield Delay(1e-6)
        print(f"in=0000000000000000, out={bin((yield not16.out))[2:].zfill(16)}")

        # Test case 2: input = 1111111111111111
        yield not16.in_.eq(0b1111111111111111)
        yield Delay(1e-6)
        print(f"in=1111111111111111, out={bin((yield not16.out))[2:].zfill(16)}")

        # Test case 3: input = 1010101010101010
        yield not16.in_.eq(0b1010101010101010)
        yield Delay(1e-6)
        print(f"in=1010101010101010, out={bin((yield not16.out))[2:].zfill(16)}")

        # Test case 4: input = 0011110011000011
        yield not16.in_.eq(0b0011110011000011)
        yield Delay(1e-6)
        print(f"in=0011110011000011, out={bin((yield not16.out))[2:].zfill(16)}")

        # Test case 5: input = 0001001000110100
        yield not16.in_.eq(0b0001001000110100)
        yield Delay(1e-6)
        print(f"in=0001001000110100, out={bin((yield not16.out))[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_not16()
