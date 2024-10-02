from amaranth import *
from amaranth.sim import *


class NorGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(~(self.a | self.b))  # NOR logic: NOT (a OR b)
        return m

def simulate_nor_gate():
    nor_gate = NorGate()
    sim = Simulator(nor_gate)

    def process():
        yield nor_gate.a.eq(0)
        yield nor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=0, b=0, out=", (yield nor_gate.out))

        yield nor_gate.a.eq(0)
        yield nor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield nor_gate.out))

        yield nor_gate.a.eq(1)
        yield nor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield nor_gate.out))

        yield nor_gate.a.eq(1)
        yield nor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield nor_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_nor_gate()