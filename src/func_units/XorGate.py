from amaranth import *
from amaranth.sim import *


class XorGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(self.a ^ self.b)  # XOR logic: a XOR b
        return m
    
# Example: Simulating XOR Gate
def simulate_xor_gate():
    xor_gate = XorGate()
    sim = Simulator(xor_gate)

    def process():
        yield xor_gate.a.eq(0)
        yield xor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=0, b=0, out=", (yield xor_gate.out))

        yield xor_gate.a.eq(0)
        yield xor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield xor_gate.out))

        yield xor_gate.a.eq(1)
        yield xor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield xor_gate.out))

        yield xor_gate.a.eq(1)
        yield xor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield xor_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_xor_gate()
