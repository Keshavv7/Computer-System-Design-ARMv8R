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

# Testbench
from amaranth.sim import Simulator

# Create an instance of the RegisterMemory module with 8-bit width and 16 registers
mem = RegisterMemory(width=8, depth=16)

# Set up a simulator
sim = Simulator(mem)
sim.add_clock(1e-6)  # 1 MHz clock

# Define a simple testbench
def testbench():
    # Write 0xAB to address 0
    yield mem.addr.eq(0)
    yield mem.data_in.eq(0xAB)
    yield mem.write_en.eq(1)  # Enable write
    yield  # Wait for a clock cycle to complete the write
    
    # Disable write and read back from address 0
    yield mem.write_en.eq(0)  # Disable write (so it reads)
    yield mem.addr.eq(0)
    yield  # Wait for a clock cycle to read the data
    read_data = yield mem.data_out
    assert read_data == 0xAB, f"Expected 0xAB, got {read_data}"

    # Write 0xCD to address 1
    yield mem.addr.eq(1)
    yield mem.data_in.eq(0xCD)
    yield mem.write_en.eq(1)  # Enable write again
    yield  # Wait for a clock cycle
    
    # Read from address 1
    yield mem.write_en.eq(0)  # Disable write (so it reads)
    yield mem.addr.eq(1)
    yield  # Wait for a clock cycle to read the data
    read_data = yield mem.data_out
    assert read_data == 0xCD, f"Expected 0xCD, got {read_data}"

sim.add_process(testbench)
sim.run()

      
