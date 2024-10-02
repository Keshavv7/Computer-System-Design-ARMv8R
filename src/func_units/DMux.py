from amaranth import *
from amaranth.sim import *

class DMux(Elaboratable):
    def __init__(self):
        self.in_ = Signal()  # Input signal
        self.sel = Signal()  # Selector signal
        self.a = Signal()    # Output signal a
        self.b = Signal()    # Output signal b

    def elaborate(self, platform):
        m = Module()

        # Demux logic: If sel=0, in_ goes to a; if sel=1, in_ goes to b
        with m.If(self.sel == 0):
            m.d.comb += self.a.eq(self.in_)
            m.d.comb += self.b.eq(0)
        with m.Else():
            m.d.comb += self.b.eq(self.in_)
            m.d.comb += self.a.eq(0)

        return m


def simulate_dmux():
    dmux = DMux()
    sim = Simulator(dmux)

    def process():
        # Test case 1: in=0, sel=0 -> a=0, b=0
        yield dmux.in_.eq(0)
        yield dmux.sel.eq(0)
        yield Delay(1e-6)
        print(f"in=0, sel=0, a={yield dmux.a}, b={yield dmux.b}")

        # Test case 2: in=0, sel=1 -> a=0, b=0
        yield dmux.sel.eq(1)
        yield Delay(1e-6)
        print(f"in=0, sel=1, a={yield dmux.a}, b={yield dmux.b}")

        # Test case 3: in=1, sel=0 -> a=1, b=0
        yield dmux.in_.eq(1)
        yield dmux.sel.eq(0)
        yield Delay(1e-6)
        print(f"in=1, sel=0, a={yield dmux.a}, b={yield dmux.b}")

        # Test case 4: in=1, sel=1 -> a=0, b=1
        yield dmux.sel.eq(1)
        yield Delay(1e-6)
        print(f"in=1, sel=1, a={yield dmux.a}, b={yield dmux.b}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_dmux()
