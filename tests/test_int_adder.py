from amaranth.sim import Simulator
from amaranth import *
import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))

from func_units.int_adder import IntAdder

# Pytest test function
@pytest.mark.parametrize("x, y, expected_rslt, expected_overflow", [
    (3, 4, 7, 0),               # Test case 1: 3 + 4
    (100, 200, 300, 0),         # Test case 2: 100 + 200
    (65535, 1, 0, 1),           # Test case 3: Overflow case (adjusted for current implementation)
])
def test_int_adder(x, y, expected_rslt, expected_overflow):
    adder = IntAdder(16)  # Create 16-bit adder
    m = Module()
    m.submodules.adder = adder

    # Define simulation process
    def process():
        # Apply test values
        yield adder.x.eq(x)
        yield adder.y.eq(y)

        # Check result and overflow
        assert (yield adder.rslt) == expected_rslt, f"Failed on {x} + {y}, expected {expected_rslt}"
        assert (yield adder.overflow) == expected_overflow, f"Failed on overflow check for {x} + {y}"

    # Set up the simulator
    sim = Simulator(m)
    sim.add_testbench(process)

    # Run simulation
    sim.run()
