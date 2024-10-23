# from amaranth.sim import Simulator
# from amaranth import *
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                                 '../src/')))
# from func_units.alu_bitm import ALUB


# Testbench for ALU Bit Manipulation Operations
# async def testbench_bit_manipulation(ctx):
#     alu = ALUB()

    # Test BFC (Bit Field Clear)
#     ctx.set(alu.a, 0b1111111111111111)  # Initial value
#     ctx.set(alu.b, (2 << 5) | 4)        # Clear from bit 2, width 4
#     ctx.set(alu.alu_ctrl, 0b100000)     # BFC
#     await ctx.delay(1e-6)
#     assert ctx.get(alu.o) == 0b11111111111100001111, f"BFC failed, got {ctx.get(alu.o)}"

    # Test BFI (Bit Field Insert)
#     ctx.set(alu.a, 0b1111000011110000)  # Initial value
#     ctx.set(alu.b, (0b1010 << 5) | 4)   # Insert 0b1010 at bit 5, width 4
#     ctx.set(alu.alu_ctrl, 0b100001)     # BFI
 #    await ctx.delay(1e-6)
 #    assert ctx.get(alu.o) == 0b1111010111110000, f"BFI failed, got {ctx.get(alu.o)}"
##  
 #    # Test CLZ (Count Leading Zeros)
 #    ctx.set(alu.a, 0b0000111100000000)  # Input value
 #    ctx.set(alu.alu_ctrl, 0b100010)     # CLZ
 #    await ctx.delay(1e-6)
 #    assert ctx.get(alu.o) == 4, f"CLZ failed, got {ctx.get(alu.o)}"
# 
    # Test RBIT (Reverse Bits)
 #    ctx.set(alu.a, 0b00000000000000000000000011110000)  # Initial value
 #    ctx.set(alu.alu_ctrl, 0b100011)     # RBIT
 #    await ctx.delay(1e-6)
 #    assert ctx.get(alu.o) == 0b00001111000000000000000000000000, f"RBIT failed, got {ctx.get(alu.o)}"

    # Test REV (Byte-Reverse)
 #    ctx.set(alu.a, 0x12345678)          # Initial value
 #    ctx.set(alu.alu_ctrl, 0b100100)     # REV
 #    await ctx.delay(1e-6)
 #    assert ctx.get(alu.o) == 0x78563412, f"REV failed, got {ctx.get(alu.o)}"
# 
# Create and run the simulation
# alu = ALUB()  # Instantiate ALU
# sim = Simulator(alu)
#sim.add_clock(1e-6)  # Add a clock with a period of 1 microsecond
# # sim.add_sync_process(testbench_bit_manipulation)  # Add bit manipulation testbench
# with sim.write_vcd("alu_bit_test.vcd"):
 #    sim.run()