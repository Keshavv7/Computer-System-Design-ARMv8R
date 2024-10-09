from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class ControlUnit(Component):
    instruction: In(32)  # Full instruction
    alu_ctrl: Out(6)     # Control signal to ALU
    carry_in: Out(1)     # Carry-in signal to ALU

    def elaborate(self, platform):
        m = Module()

        # Extract fields from the instruction (assuming a simplified instruction format)
        opcode = self.instruction[26:32]  # Last 6 bits as opcode

        # Control signals (defaults)
        alu_ctrl = Signal(6, reset=0)
        carry_in = Signal(1, reset=0)

        # Define instruction to ALU mapping
        with m.Switch(opcode):
            # Arithmetic operations
            with m.Case(0b000000):  # ADD
                m.d.comb += alu_ctrl.eq(0b000000)
            with m.Case(0b000001):  # ADC (Add with Carry)
                m.d.comb += [
                    alu_ctrl.eq(0b000001),
                    carry_in.eq(1)
                ]
            with m.Case(0b000010):  # SUB
                m.d.comb += alu_ctrl.eq(0b000010)
            with m.Case(0b000011):  # SBC (Subtract with Carry)
                m.d.comb += [
                    alu_ctrl.eq(0b000011),
                    carry_in.eq(1)
                ]
            with m.Case(0b000100):  # RSB (Reverse Subtract)
                m.d.comb += alu_ctrl.eq(0b000100)
            with m.Case(0b000101):  # RSC (Reverse Subtract with Carry)
                m.d.comb += [
                    alu_ctrl.eq(0b000101),
                    carry_in.eq(1)
                ]

            # Multiplication instructions
            with m.Case(0b000110):  # MUL (Multiply)
                m.d.comb += alu_ctrl.eq(0b000110)
            with m.Case(0b000111):  # MLA (Multiply and Accumulate)
                m.d.comb += alu_ctrl.eq(0b000111)
            with m.Case(0b001000):  # MLS (Multiply and Subtract)
                m.d.comb += alu_ctrl.eq(0b001000)

            # Division instruction
            with m.Case(0b001001):  # sDIV (Signed Divide)
                m.d.comb += alu_ctrl.eq(0b001001)

            # Logical instructions
            with m.Case(0b001010):  # AND
                m.d.comb += alu_ctrl.eq(0b001010)
            with m.Case(0b001011):  # ORR (OR)
                m.d.comb += alu_ctrl.eq(0b001011)
            with m.Case(0b001100):  # EOR (XOR)
                m.d.comb += alu_ctrl.eq(0b001100)
            with m.Case(0b001101):  # BIC (Bit Clear)
                m.d.comb += alu_ctrl.eq(0b001101)
            with m.Case(0b001110):  # MVN (Move Not)
                m.d.comb += alu_ctrl.eq(0b001110)

            # Shift instructions
            with m.Case(0b001111):  # LSL (Logical Shift Left)
                m.d.comb += alu_ctrl.eq(0b001111)
            with m.Case(0b010000):  # LSR (Logical Shift Right)
                m.d.comb += alu_ctrl.eq(0b010000)
            with m.Case(0b010001):  # ASR (Arithmetic Shift Right)
                m.d.comb += alu_ctrl.eq(0b010001)
            with m.Case(0b010010):  # ROR (Rotate Right)
                m.d.comb += alu_ctrl.eq(0b010010)
            with m.Case(0b010011):  # RRX (Rotate Right with Extend)
                m.d.comb += alu_ctrl.eq(0b010011)

            # Compare instructions
            with m.Case(0b010100):  # CMP (Compare: rn - op2)
                m.d.comb += alu_ctrl.eq(0b010100)
            with m.Case(0b010101):  # CMN (Compare Negative: rn + op2)
                m.d.comb += alu_ctrl.eq(0b010101)

        # Assign the control signals
        m.d.comb += [
            self.alu_ctrl.eq(alu_ctrl),
            self.carry_in.eq(carry_in)
        ]

        return m