from amaranth import *
from amaranth.sim import *

class And8Gate(Elaboratable):
    def __init__(self):
        # Define 8-bit input signals
        self.a = Signal(8)  # 8-bit input 'a'
        self.b = Signal(8)  # 8-bit input 'b'
        self.out = Signal(8)  # 8-bit output 'out'

    def elaborate(self, platform):
        m = Module()

        # Perform bitwise AND for each bit of the 8-bit inputs
        m.d.comb += self.out.eq(self.a & self.b)  # Bitwise AND

        return m

# Simulation function
def simulate_and8_gate():
    and8_gate = And8Gate()
    sim = Simulator(and8_gate)

    def process():
        # Test case 1: a = 00000000, b = 00000000
        yield and8_gate.a.eq(0b00000000)
        yield and8_gate.b.eq(0b00000000)
        yield Delay(1e-6)
        print(f"a=00000000, b=00000000, out={bin((yield and8_gate.out))[2:].zfill(8)}")

        # Test case 2: a = 00000000, b = 11111111
        yield and8_gate.a.eq(0b00000000)
        yield and8_gate.b.eq(0b11111111)
        yield Delay(1e-6)
        print(f"a=00000000, b=11111111, out={bin((yield and8_gate.out))[2:].zfill(8)}")

        # Test case 3: a = 11111111, b = 11111111
        yield and8_gate.a.eq(0b11111111)
        yield and8_gate.b.eq(0b11111111)
        yield Delay(1e-6)
        print(f"a=11111111, b=11111111, out={bin((yield and8_gate.out))[2:].zfill(8)}")

        # Test case 4: a = 10101010, b = 01010101
        yield and8_gate.a.eq(0b10101010)
        yield and8_gate.b.eq(0b01010101)
        yield Delay(1e-6)
        print(f"a=10101010, b=01010101, out={bin((yield and8_gate.out))[2:].zfill(8)}")

        # Test case 5: a = 00111100, b = 00001111
        yield and8_gate.a.eq(0b00111100)
        yield and8_gate.b.eq(0b00001111)
        yield Delay(1e-6)
        print(f"a=00111100, b=00001111, out={bin((yield and8_gate.out))[2:].zfill(8)}")

        # Test case 6: a = 00010010, b = 10011000
        yield and8_gate.a.eq(0b00010010)
        yield and8_gate.b.eq(0b10011000)
        yield Delay(1e-6)
        print(f"a=00010010, b=10011000, out={bin((yield and8_gate.out))[2:].zfill(8)}")

    # Add process and run the simulation
    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_and8_gate()
