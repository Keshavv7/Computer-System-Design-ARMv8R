from amaranth import *
from amaranth.sim import *

class NotGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(~self.a)  # NOT logic: NOT a
        return m


    
# Example: Simulating OR Gate
def simulate_not_gate():
    not_gate = NotGate()
    sim = Simulator(not_gate)

    def process():
        yield not_gate.a.eq(0)
        yield Delay(1e-6)
        print("a=0, out=", (yield not_gate.out))

        yield not_gate.a.eq(1)
        yield Delay(1e-6)
        print("a=1, out=", (yield not_gate.out))

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_not_gate()
