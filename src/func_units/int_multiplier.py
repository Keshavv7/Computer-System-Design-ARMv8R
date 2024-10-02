from amaranth import *


class IntMultiplier(Elaboratable):
    def __init__(self, bits: int) -> None:
        super().__init__()
        self.bits = bits

        self.x = Signal(bits)
        self.y = Signal(bits)
        self.rslt = Signal(bits)
        self.overflow = Signal(1)

    def elaborate(self, platform):
        inter = Signal(2*self.bits)
        m = Module()
        m.d.comb += inter.eq(self.x*self.y)
        m.d.comb += self.rslt.eq(inter[self.bits:])
        m.d.comb += self.overflow.eq(inter[:self.bits].any())
        return m
