from amaranth import *
from amaranth.lib.wiring import Component, In, Out

class ALUB(Component):
    a: In(32)       # Operand 1 (rn)
    b: In(32)       # Operand 2 (op2)
    alu_ctrl: In(6) # Control signal to choose operation (6 bits to cover all instructions)
    carry_in: In(1) # Carry input for ADC, SBC, etc.
    o: Out(32)      # Result of ALU operation
    carry_out: Out(1) # Carry output

    def elaborate(self, platform):
        m = Module()

        # ALU result signal
        result = Signal(32)
        carry_out = Signal()

        # Define operations
        with m.Switch(self.alu_ctrl):
            # Bit manipulation instructions
            with m.Case(0b100000):  # BFC (Bit Field Clear)
                lsb = self.b[:5]  # Use `b` to determine LSB (b contains LSB and width)
                width = self.b[5:10]  # Width of the field to clear
                mask = ~(Const(1 << width) - 1 << lsb)  # Construct mask using Const
                m.d.comb += result.eq(self.a & mask)

            with m.Case(0b100001):  # BFI (Bit Field Insert)
                lsb = self.b[:5]  # Use `b` to determine LSB (b contains LSB and width)
                width = self.b[5:10]  # Width of the field to insert
                mask = Const((1 << width) - 1) << lsb  # Construct mask using Const
                m.d.comb += result.eq((self.a & ~mask) | ((self.b << lsb) & mask))

            with m.Case(0b100010):  # CLZ (Count Leading Zeros)
                clz_count = Signal(32)
                for i in range(32):
                    with m.If(self.a[i] == 1):
                        m.d.comb += clz_count.eq(31 - i)
                        break
                m.d.comb += result.eq(clz_count)

            with m.Case(0b100011):  # RBIT (Reverse Bits)
                reversed_bits = Signal(32)
                for i in range(32):
                    m.d.comb += reversed_bits[i].eq(self.a[31 - i])
                m.d.comb += result.eq(reversed_bits)

            with m.Case(0b100100):  # REV (Byte-Reverse)
                m.d.comb += result.eq(Cat(self.a[24:32], self.a[16:24], self.a[8:16], self.a[0:8]))

        # Set the output result and carry_out
        m.d.comb += [
            self.o.eq(result),
            self.carry_out.eq(carry_out)
        ]

        return m
