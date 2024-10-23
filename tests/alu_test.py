from amaranth import *
from amaranth.sim import Simulator
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../src/')))
from func_units.alu import ALU

alu = ALU()
# Testbench for ALU
async def testbench(ctx):

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

    ctx.set(alu.a, 0b0001)  # 1
    ctx.set(alu.b, 2)       # Shift left by 2
    ctx.set(alu.alu_ctrl, 0b001111)  # LSL
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0100, f"LSL failed, expected 0b0100, got {ctx.get(alu.o)}"

    # Test Logical Shift Right (LSR)
    ctx.set(alu.a, 0b1000)  # 8
    ctx.set(alu.b, 2)       # Shift right by 2
    ctx.set(alu.alu_ctrl, 0b010000)  # LSR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0010, f"LSR failed, expected 0b0010, got {ctx.get(alu.o)}"

    # Test Arithmetic Shift Right (ASR)
    ctx.set(alu.a, -16)  
    ctx.set(alu.b, 2)           # Shift right by 2
    ctx.set(alu.alu_ctrl, 0b010001)  # ASR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == -4, f"ASR failed, expected 0b11111100, got {ctx.get(alu.o)}" #TODO: Fix ASR

    # Test Rotate Right (ROR)
    ctx.set(alu.a, 0b1100)  # 12
    ctx.set(alu.b, 2)       # Rotate right by 2
    ctx.set(alu.alu_ctrl, 0b010010)  # ROR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0011, f"ROR failed, expected 0b0011, got {ctx.get(alu.o)}"

# Create and run the simulation
# Instantiate ALU
sim = Simulator(alu)
#sim.add_clock(1e-6)  # Add a clock with a period of 1 microsecond
sim.add_testbench(testbench)  # Add testbench
sim.run()
print("alu tests passed successfully!")

