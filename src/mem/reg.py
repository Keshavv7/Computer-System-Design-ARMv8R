from amaranth import *

class RegisterFile(Elaboratable):
    def __init__(self, num_regs=16, width=32):
        self.num_regs = num_regs
        self.width = width

        # Signals for register addresses, data, and control
        self.read_addr1 = Signal(range(num_regs))  # Address for the first read port
        self.read_addr2 = Signal(range(num_regs))  # Address for the second read port
        self.write_addr = Signal(range(num_regs))  # Address for the write port
        self.write_data = Signal(width)            # Data to write
        self.write_enable = Signal()               # Write enable signal

        # Outputs for reading data
        self.read_data1 = Signal(width)            # Data read from the first port
        self.read_data2 = Signal(width)            # Data read from the second port

        # Internal register storage
        self.regs = [Signal(width, reset=0) for _ in range(num_regs)]

    def elaborate(self, platform):
        m = Module()

        # Read logic using Mux for selecting based on read address
        m.d.comb += [
            self.read_data1.eq(Mux(self.read_addr1, *self.regs)),
            self.read_data2.eq(Mux(self.read_addr2, *self.regs))
        ]

        # Synchronous write logic
        with m.If(self.write_enable):
            m.d.sync += self.regs[self.write_addr].eq(self.write_data)

        return m
