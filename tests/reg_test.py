# Testbench
from amaranth.sim import Simulator
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from mem.reg import RegisterFile


def test_register():
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

    sim.add_sync_process(testbench)
    sim.run()
