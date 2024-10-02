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


def simulate_half_adder():
    half_adder = HalfAdder()
    sim = Simulator(half_adder)

    def process():
        # Test cases for the half adder
        test_cases = [
            (0, 0),  # a = 0, b = 0
            (0, 1),  # a = 0, b = 1
            (1, 0),  # a = 1, b = 0
            (1, 1),  # a = 1, b = 1
        ]

        for a, b in test_cases:
            yield half_adder.a.eq(a)
            yield half_adder.b.eq(b)
            yield Delay(1e-6)
            print(f"a={a}, b={b}, sum={yield half_adder.sum}, carry={yield half_adder.carry}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_half_adder()