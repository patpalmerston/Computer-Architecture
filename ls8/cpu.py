"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul
        }
    # takes the address of RAM returns that value

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
    # used to halt cpu and exit the emulation

    def hlt(self, op_a, op_b):
        return(0, False)
    # loading current store of

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        return (3, True)

    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        return (2, True)

    def mul(self, op_a, op_b):
        # call alu
        self.alu("MUL", op_a, op_b)
        return (3, True)

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        with open(program) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()

                try:
                    self.ram_write(int(num, 2), address)
                    address += 1
                except ValueError:
                    print('Value Error')
                    pass

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # read memory in reg and stor in 'IR'
        running = True

        while running:

            ir = self.ram[self.pc]

            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            try:
                operation_output = self.commands[ir](op_a, op_b)
                running = operation_output[1]
                self.pc += operation_output[0]

            except:
                print(f"not working: {ir}")
                sys.exit()
