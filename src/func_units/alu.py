from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class ALU(Component):
    a: In(signed(32))       # Operand 1 (rn)
    b: In(signed(32))       # Operand 2 (op2)
    alu_ctrl: In(6)         # Control signal to choose operation (6 bits to cover all instructions)
    o: Out(signed(32))      # self.o of ALU operation
    carry_out: Out(1)       # Carry output

    def elaborate(self, platform):
        m = Module()

        # Define operations
        with m.Switch(self.alu_ctrl):
            # Arithmetic operations
            with m.Case(0b000000):  # ADD
                m.d.comb += [
                    self.o.eq(self.a + self.b),
                    self.carry_out.eq(self.a + self.b > 0xFFFFFFFF)  # Carry if overflow occurs
                ]
            with m.Case(0b000010):  # SUB
                m.d.comb += [
                    self.o.eq(self.a - self.b),
                    self.carry_out.eq(self.a < self.b)  # Carry if borrow occurs
                ]

            # Multiplication instructions
            with m.Case(0b000110):  # MUL (Multiply)
                m.d.comb += self.o.eq(self.a * self.b)

            # Division instructions
            with m.Case(0b001001):  # sDIV (Signed Divide)
                m.d.comb += self.o.eq(self.a.as_signed() // self.b.as_signed())

            # Logical instructions
            with m.Case(0b001010):  # AND
                m.d.comb += self.o.eq(self.a & self.b)
            with m.Case(0b001011):  # ORR (OR)
                m.d.comb += self.o.eq(self.a | self.b)
            with m.Case(0b001100):  # EOR (XOR)
                m.d.comb += self.o.eq(self.a ^ self.b)
            with m.Case(0b001110):  # MVN (Move Not)
                m.d.comb += self.o.eq(~self.b)

            # Shift instructions
            with m.Case(0b001111):  # LSL (Logical Shift Left)
                m.d.comb += self.o.eq(self.a << (self.b[:5].as_unsigned()))  # Limit shift to 0-31
            with m.Case(0b010000):  # LSR (Logical Shift Right)
                m.d.comb += self.o.eq(self.a.as_unsigned() >> (self.b[:5].as_unsigned()))
            with m.Case(0b010001):  # ASR (Arithmetic Shift Right)
                m.d.comb += self.o.eq(self.a.as_signed() >> (self.b[:5].as_unsigned()))

            # Compare instructions (CMP)
            with m.Case(0b010100):  # CMP (Compare: rn - op2)
                m.d.comb += [
                    self.o.eq(self.a - self.b),
                    self.carry_out.eq(self.a < self.b)  # Carry if borrow
                ]

        return m
    
if __name__ == "__main__":
    from amaranth.back import verilog
    alu = ALU()
    print(verilog.convert(alu, ports=[alu.a, alu.b, alu.alu_ctrl, alu.carry_out, alu.o], emit_src=False))
