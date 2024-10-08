from amaranth import *

class RegisterMemory(Elaboratable):
    def __init__(self, width, depth):
        # Parameters for memory width (bit width) and depth (number of registers)
        self.width = width
        self.depth = depth
        
        # Memory inputs and outputs
        self.addr = Signal(range(depth))   # Address to read/write
        self.data_in = Signal(width)       # Data to be written to memory
        self.data_out = Signal(width)      # Data read from memory
        self.write_en = Signal()           # Write enable signal (1 = write, 0 = read)
    
    def elaborate(self, platform):
        m = Module()
        
        # Create an array of registers, initialized to 0
        memory = [Signal(self.width, reset=0) for _ in range(self.depth)]
        
        # Define synchronous write behavior (only writes if write_en is high)
        with m.If(self.write_en):
            # Write the input data to the selected memory register
            m.d.sync += memory[self.addr].eq(self.data_in)
        
        # Define combinational read behavior (always reads from memory)
        m.d.comb += self.data_out.eq(memory[self.addr])
        
        return m
