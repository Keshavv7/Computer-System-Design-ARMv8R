from amaranth import *
from amaranth.sim import *

class Or8Way(Elaboratable):
    def __init__(self):
        self.in_ = Signal(8)  # 8-bit input
        self.out = Signal()    # Single-bit output

    def elaborate(self, platform):
        m = Module()

        # Implementing the OR chain using 3 levels of OR logic
        w1 = Signal()
        w2 = Signal()
        w3 = Signal()
        w4 = Signal()
        w5 = Signal()
        w6 = Signal()

        # First level
        m.d.comb += w1.eq(self.in_[0] | self.in_[1])
        m.d.comb += w2.eq(self.in_[2] | self.in_[3])
        m.d.comb += w3.eq(self.in_[4] | self.in_[5])
        m.d.comb += w4.eq(self.in_[6] | self.in_[7])

        # Second level
        m.d.comb += w5.eq(w1 | w2)
        m.d.comb += w6.eq(w3 | w4)

        # Final output
        m.d.comb += self.out.eq(w5 | w6)

        return m

def simulate_or8way():
    or8way = Or8Way()
    sim = Simulator(or8way)

    def process():
        # Test case 1: in = 0b00000000 -> out = 0
        yield or8way.in_.eq(0b00000000)
        yield Delay(1e-6)
        print(f"in=00000000, out={yield or8way.out}")

        # Test case 2: in = 0b11111111 -> out = 1
        yield or8way.in_.eq(0b11111111)
        yield Delay(1e-6)
        print(f"in=11111111, out={yield or8way.out}")

        # Test case 3: in = 0b00010000 -> out = 1
        yield or8way.in_.eq(0b00010000)
        yield Delay(1e-6)
        print(f"in=00010000, out={yield or8way.out}")

        # Test case 4: in = 0b00000001 -> out = 1
        yield or8way.in_.eq(0b00000001)
        yield Delay(1e-6)
        print(f"in=00000001, out={yield or8way.out}")

        # Test case 5: in = 0b00100110 -> out = 1
        yield or8way.in_.eq(0b00100110)
        yield Delay(1e-6)
        print(f"in=00100110, out={yield or8way.out}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_or8way()
