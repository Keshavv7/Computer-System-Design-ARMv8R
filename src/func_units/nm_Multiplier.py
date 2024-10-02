from amaranth import *
from amaranth.sim import *


class NMbitMultiplier(Elaboratable):
    def __init__(self, n, m):
        self.n = n                # Number of bits in multiplicand
        self.m = m                # Number of bits in multiplier
        self.a = Signal(n)         # n-bit multiplicand
        self.b = Signal(m)         # m-bit multiplier
        self.out = Signal(n + m)   # Output will be (n + m)-bit

    def elaborate(self, platform):
        m = Module()

        # Create a signal to hold the intermediate partial sums
        partial_sums = [Signal(self.n + self.m) for _ in range(self.n)]
        
        # Generate partial products
        for i in range(self.n):
            # Create the partial product (a[i] AND all bits of b)
            partial_product = Signal(self.m)
            m.d.comb += partial_product.eq(self.a[i] * self.b)

            # Shift the partial product by the position of the current bit in a
            m.d.comb += partial_sums[i].eq(Cat(Const(0, i), partial_product, Const(0, self.n - i - 1)))

        # Add the partial products together to get the final product
        result = Signal(self.n + self.m)
        m.d.comb += result.eq(partial_sums[0])

        for i in range(1, self.n):
            result = result + partial_sums[i]

        m.d.comb += self.out.eq(result)
        
        return m

# Example Testbench

def simulate_n_m_bit_multiplier(n, m):
    multiplier = NMbitMultiplier(n, m)
    sim = Simulator(multiplier)

    def process():
        # Test cases for the n*m bit multiplier
        test_cases = [
            (0b0000, 0b0000),  # 0 * 0
            (0b0011, 0b0011),  # 3 * 3
            (0b1010, 0b1101),  # 10 * 13
            (0b1111, 0b0001),  # 15 * 1
            (0b0101, 0b0110),  # 5 * 6
        ]

        for a, b in test_cases:
            yield multiplier.a.eq(a)
            yield multiplier.b.eq(b)
            yield Delay(1e-6)
            print(f"a={bin(a)[2:].zfill(n)}, b={bin(b)[2:].zfill(m)}, product={bin((yield multiplier.out))[2:].zfill(n+m)}")

    sim.add_process(process)
    sim.run()

# Run the simulation for a 4x4-bit multiplier
simulate_n_m_bit_multiplier(4, 4)
