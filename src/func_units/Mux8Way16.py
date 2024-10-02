from amaranth import *

# Define a 16-bit 2-way Mux (equivalent to CS21B061Mux16)
class Mux16(Elaboratable):
    def __init__(self):
        self.a = Signal(16)   # 16-bit input 'a'
        self.b = Signal(16)   # 16-bit input 'b'
        self.sel = Signal()   # 1-bit selector
        self.out = Signal(16) # 16-bit output 'out'

    def elaborate(self, platform):
        m = Module()

        # Mux logic: if sel=0, output 'a'; if sel=1, output 'b'
        m.d.comb += self.out.eq(Mux(self.sel, self.b, self.a))

        return m

# Define the 8-way 16-bit Mux (equivalent to CS21B061Mux8Way16)
class Mux8Way16(Elaboratable):
    def __init__(self):
        # 16-bit inputs for the 8 options
        self.a = Signal(16)
        self.b = Signal(16)
        self.c = Signal(16)
        self.d = Signal(16)
        self.e = Signal(16)
        self.f = Signal(16)
        self.g = Signal(16)
        self.h = Signal(16)
        
        # 3-bit selector
        self.sel = Signal(3)

        # 16-bit output
        self.out = Signal(16)

    def elaborate(self, platform):
        m = Module()

        # First level: select between pairs of inputs (based on sel[0])
        mux16_1 = Mux16()
        mux16_2 = Mux16()
        mux16_3 = Mux16()
        mux16_4 = Mux16()

        m.submodules.mux16_1 = mux16_1
        m.submodules.mux16_2 = mux16_2
        m.submodules.mux16_3 = mux16_3
        m.submodules.mux16_4 = mux16_4

        m.d.comb += [
            mux16_1.a.eq(self.a),
            mux16_1.b.eq(self.b),
            mux16_1.sel.eq(self.sel[0]),
            mux16_2.a.eq(self.c),
            mux16_2.b.eq(self.d),
            mux16_2.sel.eq(self.sel[0]),
            mux16_3.a.eq(self.e),
            mux16_3.b.eq(self.f),
            mux16_3.sel.eq(self.sel[0]),
            mux16_4.a.eq(self.g),
            mux16_4.b.eq(self.h),
            mux16_4.sel.eq(self.sel[0])
        ]

        # Outputs from the first level
        w1 = mux16_1.out
        w2 = mux16_2.out
        w3 = mux16_3.out
        w4 = mux16_4.out

        # Second level: select between the results of the first level (based on sel[1])
        mux16_5 = Mux16()
        mux16_6 = Mux16()

        m.submodules.mux16_5 = mux16_5
        m.submodules.mux16_6 = mux16_6

        m.d.comb += [
            mux16_5.a.eq(w1),
            mux16_5.b.eq(w2),
            mux16_5.sel.eq(self.sel[1]),
            mux16_6.a.eq(w3),
            mux16_6.b.eq(w4),
            mux16_6.sel.eq(self.sel[1])
        ]

        # Outputs from the second level
        w5 = mux16_5.out
        w6 = mux16_6.out

        # Final level: select between the results of the second level (based on sel[2])
        mux16_final = Mux16()
        m.submodules.mux16_final = mux16_final

        m.d.comb += [
            mux16_final.a.eq(w5),
            mux16_final.b.eq(w6),
            mux16_final.sel.eq(self.sel[2]),
            self.out.eq(mux16_final.out)
        ]

        return m

# Simulation example
from amaranth.sim import *

def simulate_mux8way16():
    mux8way16 = Mux8Way16()
    sim = Simulator(mux8way16)

    def process():
        # Test various input and selector combinations
        yield mux8way16.a.eq(0b1010101010101010)  # a = 1010101010101010
        yield mux8way16.b.eq(0b0101010101010101)  # b = 0101010101010101
        yield mux8way16.c.eq(0b1111111111111111)  # c = 1111111111111111
        yield mux8way16.d.eq(0b0000000000000000)  # d = 0000000000000000
        yield mux8way16.e.eq(0b0011001100110011)  # e = 0011001100110011
        yield mux8way16.f.eq(0b1100110011001100)  # f = 1100110011001100
        yield mux8way16.g.eq(0b0001001000110100)  # g = 0001001000110100
        yield mux8way16.h.eq(0b0101011001111000)  # h = 0101011001111000

        for sel in range(8):  # Test all 3-bit selector values
            yield mux8way16.sel.eq(sel)
            yield Delay(1e-6)
            print(f"sel={bin(sel)[2:].zfill(3)}, out={bin((yield mux8way16.out))[2:].zfill(16)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_mux8way16()
