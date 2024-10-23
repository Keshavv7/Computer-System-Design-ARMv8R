from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class Decoder(Component):
    instruction: In(32)     # 32-bit instruction from ROM
    select: Out(4)          # Select signal for ALU operation
    write_rd: Out(1)        # Write enable for Register File
    funct3: Out(3)          # ALU/LSU operation type
    funct7: Out(7)          # LSU-specific operation
    imm_value: Out(32)      # Immediate value for ALU/LSU
    pc_control: Out(1)      # Control signal for PC updates (branch)
    mux_control: Out(1)     # Mux control for immediate/address selection

    def elaborate(self, platform):
        m = Module()

        opcode = Signal(4)  # ARM uses first bits for opcodes
        rd = Signal(5)
        rn = Signal(5)
        rm = Signal(5)
        imm12 = Signal(12)
        funct3 = Signal(3)
        funct7 = Signal(7)
        
        # Break down instruction into fields
        m.d.comb += [
            opcode.eq(self.instruction[21:25]),  # Opcode is usually bits 21-24 in ARM
            rd.eq(self.instruction[12:16]),      # Destination register
            rn.eq(self.instruction[16:20]),      # First operand register
            rm.eq(self.instruction[0:4]),        # Second operand register or immediate
            imm12.eq(self.instruction[0:12]),    # Immediate value
            funct3.eq(self.instruction[4:7]),    # ALU/LSU operation type
            funct7.eq(self.instruction[20:27])   # LSU operation flag
        ]

        # Default values for outputs
        m.d.comb += [
            self.select.eq(0),        # Default ALU select
            self.write_rd.eq(0),      # Default: don't write to regfile
            self.funct3.eq(funct3),   # Default funct3
            self.funct7.eq(funct7),   # Default funct7
            self.imm_value.eq(imm12), # Default immediate
            self.pc_control.eq(0),    # Default: no PC control
            self.mux_control.eq(0)    # Default mux control
        ]

        # Decode based on opcode and funct3/funct7
        with m.Switch(opcode):
            # Logical Instructions
            with m.Case(0b0000):  # AND
                m.d.comb += self.select.eq(0b0000)
                m.d.comb += self.write_rd.eq(1)

            with m.Case(0b0001):  # EOR
                m.d.comb += self.select.eq(0b0001)
                m.d.comb += self.write_rd.eq(1)

            with m.Case(0b0010):  # ORR
                m.d.comb += self.select.eq(0b0010)
                m.d.comb += self.write_rd.eq(1)

            # Arithmetic Instructions
            with m.Case(0b0011):  # ADD
                m.d.comb += self.select.eq(0b0011)
                m.d.comb += self.write_rd.eq(1)

            with m.Case(0b0100):  # SUB
                m.d.comb += self.select.eq(0b0100)
                m.d.comb += self.write_rd.eq(1)

            with m.Case(0b0101):  # MUL
                m.d.comb += self.select.eq(0b0101)
                m.d.comb += self.write_rd.eq(1)

            # Load/Store Instructions
            with m.Case(0b0110):  # LDR
                m.d.comb += self.select.eq(0b0110)
                m.d.comb += self.write_rd.eq(1)
                m.d.comb += self.funct3.eq(0b001)  # Indicate load in LSU

            with m.Case(0b0111):  # STR
                m.d.comb += self.select.eq(0b0111)
                m.d.comb += self.funct3.eq(0b010)  # Indicate store in LSU

            # Branching Instructions
            with m.Case(0b1000):  # B
                m.d.comb += self.pc_control.eq(1)  # Control PC for branching

            with m.Case(0b1001):  # BEQ
                m.d.comb += self.pc_control.eq(1)
                m.d.comb += self.funct3.eq(0b000)  # Branch if equal

            with m.Case(0b1010):  # BGT
                m.d.comb += self.pc_control.eq(1)
                m.d.comb += self.funct3.eq(0b001)  # Branch if greater than

            with m.Case(0b1011):  # BLT
                m.d.comb += self.pc_control.eq(1)
                m.d.comb += self.funct3.eq(0b010)  # Branch if less than

            # MOV and immediate handling
            with m.Case(0b1100):  # MOV
                m.d.comb += self.select.eq(0b1100)
                m.d.comb += self.write_rd.eq(1)
                m.d.comb += self.mux_control.eq(1)  # Select immediate in mux

            # Push/Pop Instructions (for stack operations)
            with m.Case(0b1101):  # PUSH
                m.d.comb += self.funct3.eq(0b011)
                m.d.comb += self.write_rd.eq(0)

            with m.Case(0b1110):  # POP
                m.d.comb += self.funct3.eq(0b100)
                m.d.comb += self.write_rd.eq(1)

        return m
