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

    # Test OR
    ctx.set(alu.a, 0b1100)  # 12
    ctx.set(alu.b, 0b1010)  # 10
    ctx.set(alu.alu_ctrl, 0b0011)  # OR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b1110, f"OR failed, expected 0b1110, got {ctx.get(alu.o)}"

    # Test XOR
    ctx.set(alu.a, 0b1100)  # 12
    ctx.set(alu.b, 0b1010)  # 10
    ctx.set(alu.alu_ctrl, 0b0100)  # XOR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0110, f"XOR failed, expected 0b0110, got {ctx.get(alu.o)}"

    # Test Logical Shift Left (LSL)
    ctx.set(alu.a, 0b0001)  # 1
    ctx.set(alu.b, 2)       # Shift left by 2
    ctx.set(alu.alu_ctrl, 0b0101)  # LSL
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0100, f"LSL failed, expected 0b0100, got {ctx.get(alu.o)}"

    # Test Logical Shift Right (LSR)
    ctx.set(alu.a, 0b1000)  # 8
    ctx.set(alu.b, 2)       # Shift right by 2
    ctx.set(alu.alu_ctrl, 0b0110)  # LSR
    await ctx.delay(1e-6)
    assert ctx.get(alu.o) == 0b0010, f"LSR failed, expected 0b0010, got {ctx.get(alu.o)}"

    # Test Arithmetic Shift Right (ASR)
    ctx.set(alu.a, 0b11110000)  # -16 in signed (2's complement)
    ctx.set(alu.b, 0b00000010)  # Shift right by 2
    ctx.set(alu.alu_ctrl, 0b0111)  # ASR
    await ctx.delay(1e-6)
    #assert ctx.get(alu.o) == 0x11111100, f"ASR failed, expected 0b11111100, got {ctx.get(alu.o)}" TODO: Check this out

# Create and run the simulation
alu = ALU()  # Instantiate ALU
sim = Simulator(alu)
sim.add_testbench(testbench)
with sim.write_vcd("alu_test.vcd"):
    sim.run()

