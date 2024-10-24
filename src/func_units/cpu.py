from amaranth import *
from amaranth.lib.wiring import Component, In, Out
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../../src/')))

from func_units.alu import ALU
from func_units.decoder import Decoder
from func_units.pc_ctrl import PCControl
from mem.reg import RegisterFile

class CPU(Component):
    PCLine: Out(32)
    Instruction: In(32)

    DWriteLine: Out(32)
    DReadLine: In(32)
    DWEnable: Out(1)
    DAddr: Out(32)

    def elaborate(self, platform):
        m = Module()
        PC = Signal(32)
        CPSR = Signal(3)
        m.submodules.pcc = pcc = PCControl()
        m.submodules.dec = dec = Decoder()
        m.submodules.alu = alu = ALU()
        m.submodules.rf = rf = RegisterFile()
        m.d.sync += [pcc.PCIn.eq(PC), self.PCLine.eq(pcc.PCOut), 
                     PC.eq(pcc.PCOut), pcc.CPSR.eq(CPSR)]
        
        m.d.comb += dec.instruction.eq(self.Instruction)

        with m.If(dec.itype == 1): #Arith
            m.d.comb += rf.read_addr1.eq(dec.rm_addr)
            rval = Signal(32)
            rval2 = Signal(32)
            m.d.comb += rval.eq(rf.read_data1)
            with m.If(dec.is_imm):
                m.d.comb += rval2.eq(dec.value)
            with m.Else():
                m.d.comb += rf.read_addr2.eq(dec.value[:-4])
                m.d.comb += rval2.eq(rf.read_data2)

            
            m.d.comb += alu.a.eq(rval)
            m.d.comb += alu.b.eq(rval2)
            m.d.comb += alu.op.eq(dec.u_ctrl)  
            m.d.comb += rf.write_addr.eq(dec.rd_addr)
            m.d.comb += rf.write_data.eq(alu.o)

        return m

