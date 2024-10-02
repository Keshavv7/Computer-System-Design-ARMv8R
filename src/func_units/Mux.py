from amaranth import *
from amaranth.sim import *

class Mux(Elaboratable):
    def __init__(self):
        self.a = Signal()    # Single-bit input a
        self.b = Signal()    # Single-bit input b
        self.sel = Signal()  # Single-bit selector
        self.out = Signal()  # Single-bit output

    def elaborate(self, platform):
        m = Module()

        # Mux logic: if sel=0, out = a; if sel=1, out = b
        with m.If(self.sel == 0):
            m.d.comb += self.out.eq(self.a)
        with m.Else():
            m.d.comb += self.out.eq(self.b)

        return m

# Simulation based on the provided test script
def simulate_mux():
    mux = Mux()
    sim = Simulator(mux)

    def process():
        # Test 1: a=0, b=0, sel=0 -> out should be 0 (select a)
        yield mux.a.eq(0)
        yield mux.b.eq(0)
        yield mux.sel.eq(0)
        yield Delay(1e-6)
        print(f"a=0, b=0, sel=0, out={(yield mux.out)}")

        # Test 2: a=0, b=0, sel=1 -> out should be 0 (select b)
        yield mux.sel.eq(1)
        yield Delay(1e-6)
        print(f"a=0, b=0, sel=1, out={(yield mux.out)}")

        # Test 3: a=0, b=1, sel=0 -> out should be 0 (select a)
        yield mux.a.eq(0)
        yield mux.b.eq(1)
        yield mux.sel.eq(0)
        yield Delay(1e-6)
        print(f"a=0, b=1, sel=0, out={(yield mux.out)}")

        # Test 4: a=0, b=1, sel=1 -> out should be 1 (select b)
        yield mux.sel.eq(1)
        yield Delay(1e-6)
        print(f"a=0, b=1, sel=1, out={(yield mux.out)}")

        # Test 5: a=1, b=0, sel=0 -> out should be 1 (select a)
        yield mux.a.eq(1)
        yield mux.b.eq(0)
        yield mux.sel.eq(0)
        yield Delay(1e-6)
        print(f"a=1, b=0, sel=0, out={(yield mux.out)}")

        # Test 6: a=1, b=0, sel=1 -> out should be 0 (select b)
        yield mux.sel.eq(1)
        yield Delay(1e-6)
        print(f"a=1, b=0, sel=1, out={(yield mux.out)}")

        # Test 7: a=1, b=1, sel=0 -> out should be 1 (select a)
        yield mux.a.eq(1)
        yield mux.b.eq(1)
        yield mux.sel.eq(0)
        yield Delay(1e-6)
        print(f"a=1, b=1, sel=0, out={(yield mux.out)}")

        # Test 8: a=1, b=1, sel=1 -> out should be 1 (select b)
        yield mux.sel.eq(1)
        yield Delay(1e-6)
        print(f"a=1, b=1, sel=1, out={(yield mux.out)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_mux()
