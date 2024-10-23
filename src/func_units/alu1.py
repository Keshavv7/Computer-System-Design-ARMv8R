from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class ALU(Component):
    a: In(32)       # Operand 1 (rn)
    b: In(32)       # Operand 2 (op2)
    alu_ctrl: In(6) # Control signal to choose operation (6 bits to cover all instructions)
    carry_in: In(1) # Carry input for ADC, SBC, etc.
    o: Out(32)      # Result of ALU operation
    carry_out: Out(1) # Carry output

    def elaborate(self, platform):
        m = Module()

        # ALU result signal
        result = Signal(32).as_signed()
        carry_out = Signal()

        # Define operations
        with m.Switch(self.alu_ctrl):
            # Arithmetic operations
            with m.Case(0b000000):  # ADD
                sum_result = self.a + self.b
                m.d.comb += [
                    result.eq(sum_result),
                    carry_out.eq(sum_result > 0xFFFFFFFF)  # Carry if overflow occurs
                ]
            with m.Case(0b000001):  # ADC (Add with Carry)
                sum_result = self.a + self.b + self.carry_in
                m.d.comb += [
                    result.eq(sum_result),
                    carry_out.eq(sum_result > 0xFFFFFFFF)
                ]
            with m.Case(0b000010):  # SUB
                sub_result = self.a - self.b
                m.d.comb += [
                    result.eq(sub_result),
                    carry_out.eq(self.a < self.b)  # Carry if borrow occurs
                ]
            with m.Case(0b000011):  # SBC (Subtract with Carry)
                sub_result = self.a - (self.b + self.carry_in)
                m.d.comb += [
                    result.eq(sub_result),
                    carry_out.eq(self.a < (self.b + self.carry_in))
                ]
            with m.Case(0b000100):  # RSB (Reverse Subtract)
                sub_result = self.b - self.a
                m.d.comb += result.eq(sub_result)
            with m.Case(0b000101):  # RSC (Reverse Subtract with Carry)
                sub_result = self.b - (self.a + self.carry_in)
                m.d.comb += result.eq(sub_result)

            # Multiplication instructions
            with m.Case(0b000110):  # MUL (Multiply)
                m.d.comb += result.eq(self.a * self.b)
            with m.Case(0b000111):  # MLA (Multiply and Accumulate)
                m.d.comb += result.eq(self.a * self.b + self.carry_in)
            with m.Case(0b001000):  # MLS (Multiply and Subtract)
                m.d.comb += result.eq(self.carry_in - (self.a * self.b))

            # Division instructions
            with m.Case(0b001001):  # sDIV (Signed Divide)
                m.d.comb += result.eq(self.a.as_signed() // self.b.as_signed())

            # Logical instructions
            with m.Case(0b001010):  # AND
                m.d.comb += result.eq(self.a & self.b)
            with m.Case(0b001011):  # ORR (OR)
                m.d.comb += result.eq(self.a | self.b)
            with m.Case(0b001100):  # EOR (XOR)
                m.d.comb += result.eq(self.a ^ self.b)
            with m.Case(0b001101):  # BIC (Bit Clear)
                m.d.comb += result.eq(self.a & ~self.b)
            with m.Case(0b001110):  # MVN (Move Not)
                m.d.comb += result.eq(~self.b)

            # Shift instructions
            with m.Case(0b001111):  # LSL (Logical Shift Left)
                m.d.comb += result.eq(self.a << (self.b[:5].as_unsigned()))  # Limit shift to 0-31
            with m.Case(0b010000):  # LSR (Logical Shift Right)
                m.d.comb += result.eq(self.a >> (self.b[:5].as_unsigned()))
            with m.Case(0b010001):  # ASR (Arithmetic Shift Right)
                m.d.comb += result.eq(self.a.as_signed() >> (self.b[:5].as_unsigned()))
            with m.Case(0b010010):  # ROR (Rotate Right)
                m.d.comb += result.eq((self.a >> self.b[:5].as_unsigned()) | (self.a << (32 - self.b[:5]).as_unsigned()))
            with m.Case(0b010011):  # RRX (Rotate Right with Extend)
                m.d.comb += result.eq((self.carry_in << 31) | (self.a >> 1))

            # Compare instructions (CMP and CMN)
            with m.Case(0b010100):  # CMP (Compare: rn - op2)
                cmp_result = self.a - self.b
                m.d.comb += [
                    result.eq(cmp_result),
                    carry_out.eq(self.a < self.b)  # Carry if borrow
                ]
            with m.Case(0b010101):  # CMN (Compare Negative: rn + op2)
                cmn_result = self.a + self.b
                m.d.comb += [
                    result.eq(cmn_result),
                    carry_out.eq(cmn_result > 0xFFFFFFFF)  # Carry if overflow occurs
                ]

        # Set the output result and carry_out
        m.d.comb += [
            self.o.eq(result.as_signed()),
            self.carry_out.eq(carry_out.as_signed())
        ]

        return m
    
if __name__ == "__main__":
    from amaranth.back import verilog
    alu = ALU()
    print(verilog.convert(alu, ports=[alu.a, alu.b, alu.alu_ctrl, alu.carry_in, alu.carry_out, alu.o]))
