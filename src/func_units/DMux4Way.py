from amaranth import *

class DMux(Elaboratable):
    def __init__(self):
        self.in_ = Signal()   # Single-bit input signal
        self.sel = Signal()   # 1-bit selector
        self.a = Signal()     # First output (if sel=0)
        self.b = Signal()     # Second output (if sel=1)

    def elaborate(self, platform):
        m = Module()

        # DMux logic: if sel=0, route 'in' to 'a'; if sel=1, route 'in' to 'b'
        with m.If(self.sel == 0):
            m.d.comb += [self.a.eq(self.in_), self.b.eq(0)]
        with m.Else():
            m.d.comb += [self.a.eq(0), self.b.eq(self.in_)]

        return m

class DMux4Way(Elaboratable):
    def __init__(self):
        self.in_ = Signal()    # Single-bit input signal
        self.sel = Signal(2)   # 2-bit selector
        self.out = Signal(4)   # 4-bit output signals

    def elaborate(self, platform):
        m = Module()

        # Create two instances of the DMux for the first and second levels
        dmux1 = DMux()  # First level DMux to split by sel[1]
        dmux2a = DMux() # Second level DMux for outA (sel[0] split)
        dmux2b = DMux() # Second level DMux for outB (sel[0] split)

        # Instantiate the first DMux (splits based on sel[1])
        m.submodules.dmux1 = dmux1
        m.d.comb += [
            dmux1.in_.eq(self.in_),
            dmux1.sel.eq(self.sel[1])
        ]
        
        # First-level outputs: outA and outB (these are intermediary signals)
        outA = Signal()  # Output of DMux1 for sel[1] = 0
        outB = Signal()  # Output of DMux1 for sel[1] = 1
        m.d.comb += [
            outA.eq(dmux1.a),
            outB.eq(dmux1.b)
        ]

        # Instantiate the second-level DMux (split outA based on sel[0])
        m.submodules.dmux2a = dmux2a
        m.d.comb += [
            dmux2a.in_.eq(outA),
            dmux2a.sel.eq(self.sel[0]),
            self.out[0].eq(dmux2a.a),  # Output to out[0]
            self.out[1].eq(dmux2a.b)   # Output to out[1]
        ]

        # Instantiate the second-level DMux (split outB based on sel[0])
        m.submodules.dmux2b = dmux2b
        m.d.comb += [
            dmux2b.in_.eq(outB),
            dmux2b.sel.eq(self.sel[0]),
            self.out[2].eq(dmux2b.a),  # Output to out[2]
            self.out[3].eq(dmux2b.b)   # Output to out[3]
        ]

        return m

# Simulation Example
from amaranth.sim import *

def simulate_dmux4way():
    dmux4way = DMux4Way()
    sim = Simulator(dmux4way)

    def process():
        # Test different input and selector combinations
        for sel in range(4):  # Iterate over all 2-bit selector values
            yield dmux4way.sel.eq(sel)
            yield dmux4way.in_.eq(1)  # Test with input set to 1
            yield Delay(1e-6)
            print(f"sel={bin(sel)[2:].zfill(2)}, in=1, out={bin((yield dmux4way.out))[2:].zfill(4)}")

    sim.add_process(process)
    sim.run()

# Run the simulation
simulate_dmux4way()
