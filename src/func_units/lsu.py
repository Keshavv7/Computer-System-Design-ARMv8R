from amaranth import *
from amaranth.lib.wiring import *

class LSU(Component):
    rd_data: In(32)         # Data from register file for base register (rn)
    rm_data: In(32)         # Data from register file for second register (rm)
    value: In(15)           # Immediate value or offset
    is_imm: In(1)           # Immediate flag (1 for immediate, 0 for register offset)
    u_ctrl: In(6)           # LSU control signal (Load or Store)
    
    # Memory interface
    mem_addr: Out(32)       # Memory address
    mem_data: In(32)        # Data from memory (for LDR)
    mem_wdata: Out(32)      # Data to write to memory (for STR)
    mem_we: Out(1)          # Write enable for memory (1 for store, 0 for load)
    
    result: Out(32)         # Loaded data (from LDR) or result of STR operation

    def __init__(self):
        super().__init__()

    def connect(self, scope):
        # Calculate memory address
        mem_addr = Signal(32)

        # If is_imm is set, use immediate value; otherwise, use rm_data as offset
        with scope.If(self.is_imm == 1):
            scope.d.comb += mem_addr.eq(self.rn_data + self.value)
        with scope.Else():
            scope.d.comb += mem_addr.eq(self.rn_data + self.rm_data)

        # LSU control: u_ctrl will dictate if it's a load (LDR) or store (STR)
        with scope.Switch(self.u_ctrl):
            with scope.Case(10):  # LDR operation (u_ctrl = 10)
                scope.d.comb += [
                    self.mem_addr.eq(mem_addr),
                    self.result.eq(self.mem_data),  # Load from memory
                    self.mem_we.eq(0)  # Disable write (read-only)
                ]
            with scope.Case(11):  # STR operation (u_ctrl = 11)
                scope.d.comb += [
                    self.mem_addr.eq(mem_addr),
                    self.mem_wdata.eq(self.rm_data),  # Store rm_data to memory
                    self.mem_we.eq(1)  # Enable write
                ]

# Example usage
lsu = LSU()

# Connect it to a scope or testbench
m = Module()
m.submodules.lsu = lsu

# You would apply signals to `lsu.rn_data`, `lsu.rm_data`, `lsu.value`, etc.
