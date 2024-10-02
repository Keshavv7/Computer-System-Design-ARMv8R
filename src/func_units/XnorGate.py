from amaranth import *
from amaranth.sim import *


class XnorGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        # XNOR logic: NOT (a XOR b)
        m.d.comb += self.out.eq(~(self.a ^ self.b))
        return m

def simulate_xnor_gate():
    xnor_gate = XnorGate()
    sim = Simulator(xnor_gate)

    def process():
        yield xnor_gate.a.eq(0)
        yield xnor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=0, b=0, out=", (yield xnor_gate.out))

        yield xnor_gate.a.eq(0)
        yield xnor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield xnor_gate.out))

        yield xnor_gate.a.eq(1)
        yield xnor_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield xnor_gate.out))

        yield xnor_gate.a.eq(1)
        yield xnor_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield xnor_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_xnor_gate()