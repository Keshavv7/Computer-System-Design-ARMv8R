from amaranth import *

class RegisterFile(Elaboratable):
    def __init__(self, num_regs=16, width=32):
        self.num_regs = num_regs
        self.width = width

        self.read_addr1 = Signal(range(num_regs))  # Address for the first read port
        self.read_addr2 = Signal(range(num_regs))  # Address for the second read port
        self.write_addr = Signal(range(num_regs))  # Address for the write port
        self.write_data = Signal(width)            # Data to write
        self.write_enable = Signal()               # Write enable signal

        self.read_data1 = Signal(width)            # Data read from the first port
        self.read_data2 = Signal(width)            # Data read from the second port

        self.regs = [Signal(width, reset=0) for _ in range(num_regs)]

    def elaborate(self, platform):
        m = Module()

        # Combinational read logic using Switch and Case
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
            # Using a multiplexer to determine which register to write to
            with m.Switch(self.write_addr):
                for i in range(self.num_regs):
                    with m.Case(i):
                        m.d.sync += self.regs[i].eq(self.write_data)

        return m
