from amaranth.sim import Simulator
from amaranth import *
import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))

from func_units.int_multiplier import IntMultiplier

# Pytest test function
@pytest.mark.parametrize("x, y, expected_rslt, expected_overflow", [
    (3, 4, 12, 0),                 # Test case 1: 3 * 4
    (10, 20, 200, 0),              # Test case 2: 10 * 20
    (300, 400, 54464, 1),          # Test case 3: Overflow case
    (65535, 2, 65534, 1),          # Test case 4: Overflow case
])
def test_int_multiplier(x, y, expected_rslt, expected_overflow):
    multiplier = IntMultiplier(16)  # Create 16-bit multiplier
    m = Module()
    m.submodules.multiplier = multiplier

    # Define simulation process
    def process():
        # Apply test values
        yield multiplier.x.eq(x)
        yield multiplier.y.eq(y)

        # Check result and overflow
        assert (yield multiplier.rslt) == expected_rslt, f"Failed on {x} * {y}, expected result {expected_rslt}"
        assert (yield multiplier.overflow) == expected_overflow, f"Failed on overflow check for {x} * {y}"

    # Set up the simulator
    sim = Simulator(m)
    sim.add_testbench(process)

    # Run simulation
    sim.run()