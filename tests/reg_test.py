from amaranth import *
from amaranth.sim import Simulator

from ..mem.reg import RegisterFile

def test_register_file():
    # Write to register 1
    yield reg_file.write_addr.eq(1)
    yield reg_file.write_data.eq(0xDEADBEEF)
    yield reg_file.write_enable.eq(1)
    yield  # Write cycle
    yield reg_file.write_enable.eq(0)

    # Read from register 1
    yield reg_file.read_addr1.eq(1)
    yield  # Read cycle
    read_data = yield reg_file.read_data1
    assert read_data == 0xDEADBEEF, f"Expected 0xDEADBEEF, got {read_data}"

    # Write to register 2
    yield reg_file.write_addr.eq(2)
    yield reg_file.write_data.eq(0xCAFEBABE)
    yield reg_file.write_enable.eq(1)
    yield  # Write cycle
    yield reg_file.write_enable.eq(0)

    # Read from register 2
    yield reg_file.read_addr2.eq(2)
    yield  # Read cycle
    read_data = yield reg_file.read_data2
    assert read_data == 0xCAFEBABE, f"Expected 0xCAFEBABE, got {read_data}"

    # Read from both register 1 and 2 at the same time
    yield reg_file.read_addr1.eq(1)
    yield reg_file.read_addr2.eq(2)
    yield  # Read cycle
    read_data1 = yield reg_file.read_data1
    read_data2 = yield reg_file.read_data2
    assert read_data1 == 0xDEADBEEF, f"Expected 0xDEADBEEF, got {read_data1}"
    assert read_data2 == 0xCAFEBABE, f"Expected 0xCAFEBABE, got {read_data2}"

# Instantiate the register file
reg_file = RegisterFile(num_regs=16, width=32)

# Create a simulator
sim = Simulator(reg_file)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_process(test_register_file)

# Run the simulation
sim.run()
