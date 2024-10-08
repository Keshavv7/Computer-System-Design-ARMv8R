from amaranth import *
from amaranth.sim import Simulator
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from func_units.alu1 import ALU

# Testbench for ALU
async def testbench(ctx):
    await ctx.delay(1e-6)  # Wait for 1 microsecond

    # Test ADD
    ctx.set(alu.a, 5)
    ctx.set(alu.b, 3)
    ctx.set(alu.alu_ctrl, 0b0000)  # ADD
    await ctx.delay(1e-6)  # Wait for 1 microsecond
    assert ctx.get(alu.o) == 8, f"ADD failed, expected 8, got {ctx.get(alu.o)}"

    # Test SUB
    ctx.set(alu.a, 10)
    ctx.set(alu.b, 4)
    ctx.set(alu.alu_ctrl, 0b0001)  # SUB
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 6, f"SUB failed, expected 6, got {ctx.get(alu.o)}"

    # Test AND
    ctx.set(alu.a, 0b1100)  # 12
    ctx.set(alu.b, 0b1010)  # 10
    ctx.set(alu.alu_ctrl, 0b0010)  # AND
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b1000, f"AND failed, expected 0b1000, got {ctx.get(alu.o)}"

    # Continue adding tests for OR, XOR, and shifts...

# Create and run the simulation
alu = ALU()  # Instantiate ALU
sim = Simulator(alu)
sim.add_testbench(testbench)
with sim.write_vcd("alu_test.vcd"):
    sim.run()

