from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class ALU(Component):
    a: In(32)       # Operand 1 (32-bit input)
    b: In(32)       # Operand 2 (32-bit input)
    alu_ctrl: In(4) # Control signal to choose operation
    o: Out(32)      # Result of ALU operation

    def elaborate(self, platform):
        m = Module()

        # ALU result signal
        result = Signal(32)

        # ALU control logic
        with m.Switch(self.alu_ctrl):
            with m.Case(0b0000):  # ADD
                m.d.comb += result.eq(self.a + self.b)
            with m.Case(0b0001):  # SUB
                m.d.comb += result.eq(self.a - self.b)
            with m.Case(0b0010):  # AND
                m.d.comb += result.eq(self.a & self.b)
            with m.Case(0b0011):  # OR
                m.d.comb += result.eq(self.a | self.b)
            with m.Case(0b0100):  # XOR
                m.d.comb += result.eq(self.a ^ self.b)
            with m.Case(0b0101):  # Logical Shift Left (LSL)
                m.d.comb += result.eq(self.a << (self.b[:5]))  # Limit shift to 0-31
            with m.Case(0b0110):  # Logical Shift Right (LSR)
                m.d.comb += result.eq(self.a.as_unsigned() >> (self.b[:5]))
            with m.Case(0b0111):  # Arithmetic Shift Right (ASR)
                m.d.comb += result.eq(self.a.as_signed() >> (self.b[:5]))

        # Assign the result to the output
        m.d.comb += self.o.eq(result.as_signed())

        return m
