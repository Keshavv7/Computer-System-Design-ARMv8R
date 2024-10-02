from amaranth import *
from amaranth.sim import *

class Mux4Way16(Elaboratable):
    def __init__(self):
        self.a = Signal(16)   # 16-bit input a
        self.b = Signal(16)   # 16-bit input b
        self.c = Signal(16)   # 16-bit input c
        self.d = Signal(16)   # 16-bit input d
        self.sel = Signal(2)  # 2-bit selector
        self.out = Signal(16) # 16-bit output

    def elaborate(self, platform):
        m = Module()

        # Intermediate signals
        w1 = Signal(16)
        w2 = Signal(16)

        # First level multiplexors
        with m.If(self.sel[0] == 0):
            m.d.comb += w1.eq(self.a)
            m.d.comb += w2.eq(self.c)
        with m.Else():
            m.d.comb += w1.eq(self.b)
            m.d.comb += w2.eq(self.d)

        # Final multiplexor for sel[1]
        with m.If(self.sel[1] == 0):
            m.d.comb += self.out.eq(w1)
        with m.Else():
            m.d.comb += self.out.eq(w2)

        return m

# Example: Simulating Mux4Way16

def simulate_mux4way16():
    mux4way16 = Mux4Way16()
    sim = Simulator(mux4way16)

    def process():
        # Test case 1: all inputs = 0, sel = 0
        yield mux4way16.a.eq(0)
        yield mux4way16.b.eq(0)
        yield mux4way16.c.eq(0)
        yield mux4way16.d.eq(0)
        yield mux4way16.sel.eq(0b00)
        yield Delay(1e-6)
        print(f"sel=00, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # Test case 2: sel = 1
        yield mux4way16.sel.eq(0b01)
        yield Delay(1e-6)
        print(f"sel=01, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # Test case 3: sel = 2
        yield mux4way16.sel.eq(0b10)
        yield Delay(1e-6)
        print(f"sel=10, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # Test case 4: sel = 3
        yield mux4way16.sel.eq(0b11)
        yield Delay(1e-6)
        print(f"sel=11, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # Test case 5: different values for a, b, c, d
        yield mux4way16.a.eq(0b0001001000110100)
        yield mux4way16.b.eq(0b1001100001110110)
        yield mux4way16.c.eq(0b1010101010101010)
        yield mux4way16.d.eq(0b0101010101010101)

        # sel = 0, should output a
        yield mux4way16.sel.eq(0b00)
        yield Delay(1e-6)
        print(f"sel=00, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # sel = 1, should output b
        yield mux4way16.sel.eq(0b01)
        yield Delay(1e-6)
        print(f"sel=01, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # sel = 2, should output c
        yield mux4way16.sel.eq(0b10)
        yield Delay(1e-6)
        print(f"sel=10, out={bin((yield mux4way16.out))[2:].zfill(16)}")

        # sel = 3, should output d
        yield mux4way16.sel.eq(0b11)
        yield Delay(1e-6)
        print(f"sel=11, out={bin((yield mux4way16.out))[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_mux4way16()
