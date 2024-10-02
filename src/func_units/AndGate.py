from amaranth import *
from amaranth.sim import *

class AndGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(self.a & self.b)  
        return m

def simulate_and_gate():
    and_gate = AndGate()
    sim = Simulator(and_gate)


    def process():
        # Test different input combinations for the AND gate
        yield and_gate.a.eq(0)
        yield and_gate.b.eq(0)
        yield Delay(1e-6)  # Wait for 1 microsecond (delay)
        print("a=0, b=0, out=", (yield and_gate.out))

        yield and_gate.a.eq(0)
        yield and_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield and_gate.out))

        yield and_gate.a.eq(1)
        yield and_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield and_gate.out))

        yield and_gate.a.eq(1)
        yield and_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield and_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_and_gate()
