from amaranth import *
from amaranth.lib.wiring import *

class Decoder(Component):
    instruction: In(32)     # 32-bit instruction from ROM
    itype: Out(2)           # Instruction type: Arithmetic/Logic ; LD/ST ; B
    u_ctrl: Out(6)          # ALU/LSU control
    rn_addr: Out(4)         # Ope1 register address
    rm_addr: Out(4)         # Ope2 register address
    is_imm: Out(1)          # Ope3: Address or Imm?
    value: Out(15)          # Immediate value or Ope3 register address

    def elaborate(self, platform):
        m = Module()
        # Mapping parts of the instruction to outputs directly
        m.d.comb += [
            self.itype.eq(self.instruction[30:32]),  # bits [30:31] for instruction type
            self.u_ctrl.eq(self.instruction[24:30]),  # bits [24:29] for control signals
            self.rn_addr.eq(self.instruction[20:24]),  # bits [20:23] for rn register address
            self.rm_addr.eq(self.instruction[16:20]),  # bits [16:19] for rm register address
            self.is_imm.eq(self.instruction[15]),  # bit [15] indicates if it's immediate
            self.value.eq(self.instruction[0:15])  # bits [0:14] for immediate value or address
        ]

decoder = Decoder()
