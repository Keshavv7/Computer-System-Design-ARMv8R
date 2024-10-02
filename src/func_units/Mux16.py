from amaranth import *

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

class Mux16(Elaboratable):
    def __init__(self):
        self.a = Signal(16)  # 16-bit input a
        self.b = Signal(16)  # 16-bit input b
        self.sel = Signal()   # 1-bit selector
        self.out = Signal(16) # 16-bit output

    def elaborate(self, platform):
        m = Module()

        # Create 16 Mux instances, one for each bit
        for i in range(16):
            mux = Mux()  # Instantiate the 1-bit Mux
            m.submodules[f"mux{i}"] = mux  # Add it to submodules

            # Connect each Mux instance to the corresponding bit
            m.d.comb += [
                mux.a.eq(self.a[i]),    # Connect bit i of input a
                mux.b.eq(self.b[i]),    # Connect bit i of input b
                mux.sel.eq(self.sel),   # Connect the same selector to all Mux instances
                self.out[i].eq(mux.out) # Connect each Mux output to the corresponding bit of out
            ]

        return m

# Simulation Example
from amaranth.sim import *

def simulate_mux16():
    mux16 = Mux16()
    sim = Simulator(mux16)

    def process():
        # Test for different selector values (sel=0, sel=1)
        yield mux16.a.eq(0b1010101010101010)  # Example: input a = 0b1010101010101010
        yield mux16.b.eq(0b0101010101010101)  # Example: input b = 0b0101010101010101

        # Test with sel=0 (should output input a)
        yield mux16.sel.eq(0)
        yield Delay(1e-6)
        print(f"sel=0, out={bin((yield mux16.out))[2:].zfill(16)}")  

        # Test with sel=1 (should output input b)
        yield mux16.sel.eq(1)
        yield Delay(1e-6)
        print(f"sel=1, out={bin((yield mux16.out))[2:].zfill(16)}")  

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_mux16()
