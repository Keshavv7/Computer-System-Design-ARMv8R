from amaranth import *

class And8Gate(Elaboratable):
    def __init__(self):
        # Define 8-bit input signals
        self.a = Signal(8)  # 8-bit input 'a'
        self.b = Signal(8)  # 8-bit input 'b'
        self.out = Signal(8)  # 8-bit output 'out'

    def elaborate(self, platform):
        m = Module()

        # Perform bitwise AND for each bit of the 8-bit inputs
        m.d.comb += self.out.eq(self.a & self.b)

        return m

class And16Gate(Elaboratable):
    def __init__(self):
        # Define 16-bit input signals
        self.a = Signal(16)  # 16-bit input 'a'
        self.b = Signal(16)  # 16-bit input 'b'
        self.out = Signal(16)  # 16-bit output 'out'

    def elaborate(self, platform):
        m = Module()

        # Create two instances of 8-bit AND gates
        and8_0 = And8Gate()  # Handles the lower 8 bits
        and8_1 = And8Gate()  # Handles the upper 8 bits

        # Connect the lower 8 bits
        m.submodules.and8_0 = and8_0
        m.d.comb += [
            and8_0.a.eq(self.a[:8]),  # a[0..7]
            and8_0.b.eq(self.b[:8]),  # b[0..7]
            self.out[:8].eq(and8_0.out)  # out[0..7]
        ]

        # Connect the upper 8 bits
        m.submodules.and8_1 = and8_1
        m.d.comb += [
            and8_1.a.eq(self.a[8:]),  # a[8..15]
            and8_1.b.eq(self.b[8:]),  # b[8..15]
            self.out[8:].eq(and8_1.out)  # out[8..15]
        ]

        return m

# Simulation example
from amaranth.sim import *

def simulate_and16_gate():
    and16_gate = And16Gate()
    sim = Simulator(and16_gate)

    def process():
        # Test different input combinations for the 16-bit AND gate
        yield and16_gate.a.eq(0b0000000000000000)  # Example input for a
        yield and16_gate.b.eq(0b0000000000000000)  # Example input for b
        yield Delay(1e-6)
        print(f"a=0000000000000000, b=0000000000000000, out={bin((yield and16_gate.out))[2:].zfill(16)}")

        yield and16_gate.a.eq(0b0000000000000000)  # Example input for a
        yield and16_gate.b.eq(0b1111111111111111)  # Example input for b
        yield Delay(1e-6)
        print(f"a=0000000000000000, b=1111111111111111, out={bin((yield and16_gate.out))[2:].zfill(16)}")

        yield and16_gate.a.eq(0b1111111111111111)  # Example input for a
        yield and16_gate.b.eq(0b1111111111111111)  # Example input for b
        yield Delay(1e-6)
        print(f"a=1111111111111111, b=1111111111111111, out={bin((yield and16_gate.out))[2:].zfill(16)}")

        # Test different input combinations for the 16-bit AND gate
        yield and16_gate.a.eq(0b1010101010101010)  # Example input for a
        yield and16_gate.b.eq(0b0101010101010101)  # Example input for b
        yield Delay(1e-6)
        print(f"a=1010101010101010, b=0101010101010101, out={bin((yield and16_gate.out))[2:].zfill(16)}")

        yield and16_gate.a.eq(0b0011110011000011)  # Example input for a
        yield and16_gate.b.eq(0b0000111111110000)  # Example input for b
        yield Delay(1e-6)
        print(f"a=0011110011000011, b=0000111111110000, out={bin((yield and16_gate.out))[2:].zfill(16)}")

        yield and16_gate.a.eq(0b0001001000110100)  # Example input for a
        yield and16_gate.b.eq(0b1001100001110110)  # Example input for b
        yield Delay(1e-6)
        print(f"a=0001001000110100, b=1001100001110110, out={bin((yield and16_gate.out))[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_and16_gate()
