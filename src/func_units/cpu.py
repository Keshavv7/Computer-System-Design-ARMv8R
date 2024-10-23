from amaranth import *
from amaranth.lib.wiring import Component, In, Out
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../../src/')))

from func_units.alu import ALU
from func_units.control_unit import ControlUnit
from mem.reg import RegisterFile


class CPU(Component):
    inM: In(16)           # M value input (M = RAM[A])
    instruction: In(16)    # Instruction
    reset: In(1)           # Reset

    outM: Out(16)          # M value output
    writeM: Out(1)         # Write to M?
    addressM: Out(15)      # Address in data memory
    pc: Out(15)            # Program counter

    # def __init__(self):
    #     # Intermediate Signals
    #     self.isCInstruction = Signal()
    #     self.isAInstruction = Signal()
    #     self.loadA = Signal()
    #     self.loadD = Signal()
    #     self.outALU = Signal(16)

    def elaborate(self, platform):
        m = Module()
        # Intermediate Signals
        isCInstruction = Signal()
        isAInstruction = Signal()
        loadA = Signal()
        loadD = Signal()
        outALU = Signal(16)

        # Decode: C-instruction or A-instruction
        m.d.comb += isCInstruction.eq(self.instruction[15])   # isCInstruction = instruction[15]
        m.d.comb += isAInstruction.eq(~self.instruction[15])  # isAInstruction = !instruction[15]

        # Instantiate ALU, Registers, and Control Unit
        m.submodules.alu = alu = ALU(bits=16, ctrl_size=6)                # ALU instantiation
        m.submodules.control = control = ControlUnit()                    # Control unit instantiation
        m.submodules.reg_file = reg_file = RegisterFile(num_regs=16, width=32)  # Register file

        # Load A register: A-instruction or C-instruction destination
        isCWriteA = Signal()
        m.d.comb += isCWriteA.eq(self.instruction[15] & self.instruction[5])
        m.d.comb += loadA.eq(~self.instruction[15] | isCWriteA)

        # A Register loading based on instruction type
        inAReg = Signal(16)
        with m.If(isCWriteA):
            m.d.comb += inAReg.eq(outALU)    # C-instruction writes ALU output to A
        with m.Else():
            m.d.comb += inAReg.eq(self.instruction)  # A-instruction writes the instruction to A

        m.d.comb += reg_file.in_.eq(inAReg)
        m.d.comb += reg_file.load.eq(loadA)
        m.d.comb += self.addressM.eq(reg_file.out[:15])  # addressM from A register

        # ALU control signals and inputs
        m.d.comb += alu.x.eq(reg_file.out)            # Register file output as ALU input
        m.d.comb += alu.y.eq(Mux(self.instruction[12], self.inM, reg_file.out))  # A or M
        m.d.comb += alu.zx.eq(control.alu_ctrl[0])    # Control signals from control unit
        m.d.comb += alu.nx.eq(control.alu_ctrl[1])
        m.d.comb += alu.zy.eq(control.alu_ctrl[2])
        m.d.comb += alu.ny.eq(control.alu_ctrl[3])
        m.d.comb += alu.f.eq(control.alu_ctrl[4])
        m.d.comb += alu.no.eq(control.alu_ctrl[5])

        m.d.comb += self.outM.eq(alu.out)  # Output M from ALU

        # Write M control
        m.d.comb += self.writeM.eq(isCInstruction & self.instruction[3])

        # Program Counter control (jump logic)
        jumpToA = Signal()
        jgt = Signal()
        jeq = Signal()
        jlt = Signal()

        # Jump logic (simplified)
        m.d.comb += jgt.eq(alu.ng & self.instruction[0])
        m.d.comb += jeq.eq(~alu.ng & alu.zr & self.instruction[1])
        m.d.comb += jlt.eq(alu.ng & self.instruction[2])

        m.d.comb += jumpToA.eq(jgt | jeq | jlt)
        m.d.comb += reg_file.load.eq(isCInstruction & jumpToA)
        m.d.comb += reg_file.inc.eq(~reg_file.load)
        m.d.comb += reg_file.reset.eq(self.reset)
        m.d.comb += self.pc.eq(reg_file.out[:15])

        return m

# Top-level instantiation
if __name__ == "__main__":
    from amaranth.back import verilog
    cpu = CPU()
    print(verilog.convert(cpu, ports=[cpu.inM, cpu.instruction, cpu.reset, cpu.outM, cpu.writeM, cpu.addressM, cpu.pc]))
