from amaranth.back import verilog
from amaranth import *


class IntAdder(Elaboratable):
    def __init__(self, bits: int) -> None:
        super().__init__()
        self.bits = bits

        self.x = Signal(bits)
        self.y = Signal(bits)

        self.rslt = Signal(bits)
        self.overflow = Signal(1)

    def elaborate(self, platform) -> Module:
        m = Module()
        inter = Signal(self.bits+1)
        m.d.comb += inter.eq(self.x + self.y)
        m.d.comb += self.overflow.eq(inter[0])
        m.d.comb += self.rslt.eq(inter[1:])

        return m


alu = IntAdder(16)
print(verilog.convert(alu, ports=[alu.x, alu.y, alu.rslt, alu.overflow]))
