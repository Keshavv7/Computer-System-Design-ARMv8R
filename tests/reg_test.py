import sys
import os
from amaranth import *
from amaranth.sim import Simulator, Tick
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from mem.reg import RegisterFile

def test_register_file():
    yield reg_file.write_addr.eq(1)
    yield reg_file.write_data.eq(0xBEEF)
    yield reg_file.write_enable.eq(1)
    yield Tick()  # Write cycle
    yield reg_file.write_enable.eq(0)

    yield reg_file.read_addr1.eq(1)
    yield Tick()  # Read cycle
    read_data = yield reg_file.read_data1
    assert read_data == 0xBEEF, f"Expected 0xBEEF, got {read_data}"

    yield reg_file.write_addr.eq(2)
    yield reg_file.write_data.eq(0xBABE)
    yield reg_file.write_enable.eq(1)
    yield Tick()  # Write cycle
    yield reg_file.write_enable.eq(0)

    yield reg_file.read_addr2.eq(2)
    yield Tick()  # Read cycle
    read_data = yield reg_file.read_data2
    assert read_data == 0xBABE, f"Expected 0xBABE, got {read_data}"

    yield reg_file.read_addr1.eq(1)
    yield reg_file.read_addr2.eq(2)
    yield Tick()  # Read cycle
    read_data1 = yield reg_file.read_data1
    read_data2 = yield reg_file.read_data2
    assert read_data1 == 0xBEEF, f"Expected 0xBEEF, got {read_data1}"
    assert read_data2 == 0xBABE, f"Expected 0xBABE, got {read_data2}"

# Instantiate the register file
reg_file = RegisterFile()

# Create a simulator
sim = Simulator(reg_file)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_process(test_register_file)

# Run the simulation
sim.run()

