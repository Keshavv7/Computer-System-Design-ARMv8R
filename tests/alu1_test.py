from amaranth import *
from amaranth.sim import Simulator
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from func_units.alu1 import ALU

# Testbench for ALU
async def testbench(ctx):
    alu = ALU()

    # Test ADD
    ctx.set(alu.a, 5)
    ctx.set(alu.b, 3)
    ctx.set(alu.alu_ctrl, 0b000000)  # ADD
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 8, f"ADD failed, expected 8, got {ctx.get(alu.o)}"

    # Test SUB
    ctx.set(alu.a, 10)
    ctx.set(alu.b, 4)
    ctx.set(alu.alu_ctrl, 0b000010)  # SUB
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 6, f"SUB failed, expected 6, got {ctx.get(alu.o)}"

    # Test CMP (a - b)
    ctx.set(alu.a, 10)
    ctx.set(alu.b, 5)
    ctx.set(alu.alu_ctrl, 0b010100)  # CMP
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 5, f"CMP failed, expected 5, got {ctx.get(alu.o)}"

