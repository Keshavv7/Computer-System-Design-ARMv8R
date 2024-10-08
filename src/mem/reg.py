class RegisterFile(Elaboratable):
    def __init__(self, num_regs=16, width=32):
        # Parameterized number of registers and width
        self.num_regs = num_regs
        self.width = width

        # Signals
        self.read_addr1 = Signal(range(num_regs))  # Address for the first read port
        self.read_addr2 = Signal(range(num_regs))  # Address for the second read port
        self.write_addr = Signal(range(num_regs))  # Address for the write port
        self.write_data = Signal(width)            # Data to write
        self.write_enable = Signal()               # Write enable signal

        # Outputs
        self.read_data1 = Signal(width)            # Data read from first read port
        self.read_data2 = Signal(width)            # Data read from second read port

        # Internal register storage
        self.regs = [Signal(width, reset=0) for _ in range(num_regs)]

    def elaborate(self, platform):
        m = Module()

        # Combinational read from registers
        m.d.comb += [
            self.read_data1.eq(self.regs[self.read_addr1]),
            self.read_data2.eq(self.regs[self.read_addr2])
        ]

        # Synchronous write to registers
        with m.If(self.write_enable):
            m.d.sync += self.regs[self.write_addr].eq(self.write_data)

        return m
