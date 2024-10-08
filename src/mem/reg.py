from amaranth import *

class RegisterFile(Elaboratable):
    def __init__(self, num_regs=16, width=32):
        self.num_regs = num_regs
        self.width = width

        self.read_addr1 = Signal(range(num_regs))
        self.read_addr2 = Signal(range(num_regs))
        self.write_addr = Signal(range(num_regs))
        self.write_data = Signal(width)
        self.write_enable = Signal()

        self.read_data1 = Signal(width)
        self.read_data2 = Signal(width)

        self.regs = [Signal(width, reset=0) for _ in range(num_regs)]

    def elaborate(self, platform):
        m = Module()

        # Combinational read logic using Case statements
        with m.Switch(self.read_addr1):
            for i in range(self.num_regs):
                with m.Case(i):
                    m.d.comb += self.read_data1.eq(self.regs[i])

        with m.Switch(self.read_addr2):
            for i in range(self.num_regs):
                with m.Case(i):
                    m.d.comb += self.read_data2.eq(self.regs[i])

        # Synchronous write logic
        with m.If(self.write_enable):
            m.d.sync += self.regs[self.write_addr].eq(self.write_data)

        return m

