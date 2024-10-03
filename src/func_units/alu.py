from amaranth.back import verilog
from amaranth import *

# Binary: +, *, -, //, x, &, |, <<, >>, +>>
# Unary: ~


class ALU(Elaboratable):
    def __init__(self, bits, ctrl_size) -> None:
        super().__init__()
        self.ctrl_signal = Signal(ctrl_size)
        self.x = Signal(bits)
        self.y = Signal(bits)
        self.out = Signal(bits)
        self.bits = bits

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.out.eq(Mux(self.ctrl_signal[0],
                                    Mux(self.ctrl_signal[1],
                                        self.y + self.x, self.x * self.y),
                                    Mux(self.ctrl_signal[1],
                                        self.x // self.y, self.y | self.x)))

        return m
