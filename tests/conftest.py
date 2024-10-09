# conftest.py
import pytest
from amaranth.sim import Simulator
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from func_units.alu1 import ALU

# Fixture to provide 'ctx' as a simulation context
@pytest.fixture
def ctx():
    dut = ALU()

    # Setup the simulator with the DUT
    sim = Simulator(dut)  # Add a 1 MHz clock

    # Return the simulator as the context
    return sim

pytest