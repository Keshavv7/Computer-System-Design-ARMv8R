from amaranth import *
from amaranth.sim import *


class OrGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(self.a | self.b)  # OR logic: a OR b
        return m

# Example: Simulating OR Gate
def simulate_or_gate():
    or_gate = OrGate()
    sim = Simulator(or_gate)

    def process():
        yield or_gate.a.eq(0)
        yield or_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=0, b=0, out=", (yield or_gate.out))

        yield or_gate.a.eq(0)
        yield or_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield or_gate.out))

        yield or_gate.a.eq(1)
        yield or_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield or_gate.out))

        yield or_gate.a.eq(1)
        yield or_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield or_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_or_gate()
