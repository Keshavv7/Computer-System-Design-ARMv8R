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


def simulate_not8():
    not8 = Not8()
    sim = Simulator(not8)

    def process():
        # Test case 1: input = 00000000
        yield not8.in_.eq(0b00000000)
        yield Delay(1e-6)
        print(f"in=00000000, out={bin((yield not8.out))[2:].zfill(8)}")

        # Test case 2: input = 11111111
        yield not8.in_.eq(0b11111111)
        yield Delay(1e-6)
        print(f"in=11111111, out={bin((yield not8.out))[2:].zfill(8)}")

        # Test case 3: input = 10101010
        yield not8.in_.eq(0b10101010)
        yield Delay(1e-6)
        print(f"in=10101010, out={bin((yield not8.out))[2:].zfill(8)}")

        # Test case 4: input = 00111100
        yield not8.in_.eq(0b00111100)
        yield Delay(1e-6)
        print(f"in=00111100, out={bin((yield not8.out))[2:].zfill(8)}")

        # Test case 5: input = 00010010
        yield not8.in_.eq(0b00010010)
        yield Delay(1e-6)
        print(f"in=00010010, out={bin((yield not8.out))[2:].zfill(8)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_not8()
