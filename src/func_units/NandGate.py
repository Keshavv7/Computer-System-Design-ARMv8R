from amaranth import *
from amaranth.sim import *

class NandGate(Elaboratable):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(~(self.a & self.b))  # NAND logic: NOT (a AND b)
        return m


    # No need for a clock domain, since this is purely combinational logic

def simulate_nand_gate():
    nand_gate = NandGate()
    sim = Simulator(nand_gate)

    # No need for a clock domain, since this is purely combinational logic

    def process():
        # Test different input combinations for the AND gate
        yield nand_gate.a.eq(0)
        yield nand_gate.b.eq(0)
        yield Delay(1e-6)  # Wait for 1 microsecond (delay)
        print("a=0, b=0, out=", (yield nand_gate.out))

        yield nand_gate.a.eq(0)
        yield nand_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=0, b=1, out=", (yield nand_gate.out))

        yield nand_gate.a.eq(1)
        yield nand_gate.b.eq(0)
        yield Delay(1e-6)
        print("a=1, b=0, out=", (yield nand_gate.out))

        yield nand_gate.a.eq(1)
        yield nand_gate.b.eq(1)
        yield Delay(1e-6)
        print("a=1, b=1, out=", (yield nand_gate.out))

    # Use add_process (instead of add_sync_process) for combinational logic
    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_nand_gate()