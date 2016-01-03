#!/usr/bin/env python3
# http://adventofcode.com/day/23

def parse_input(inp):
    program = []

    def word(w):
        w = w.strip(',')
        if w.startswith(("-", "+")):
            return int(w)
        return w

    for line in inp:
        program.append(list(map(word, line.split())))

    return program

with open("day23_input.txt", "r") as inp:
    program = parse_input(inp)


class Machine:
    def __init__(self):
        self.a = self.b = 0

    def run(self, program):
        pc = 0
        while 0 <= pc < len(program):
            inst = program[pc]
            if 0:
                print("a = {0.a}, b = {0.b}, pc = {1} {2}".format(self, pc, inst))
            op = inst[0]
            if op == 'hlf':
                setattr(self, inst[1], getattr(self, inst[1]) // 2)
                pc += 1
            elif op == 'tpl':
                setattr(self, inst[1], getattr(self, inst[1]) * 3)
                pc += 1
            elif op == 'inc':
                setattr(self, inst[1], getattr(self, inst[1]) + 1)
                pc += 1
            elif op == 'jmp':
                pc += inst[1]
            elif op == 'jie':
                if getattr(self, inst[1]) % 2 == 0:
                    pc += inst[2]
                else:
                    pc += 1
            elif op == 'jio':
                if getattr(self, inst[1]) == 1:
                    pc += inst[2]
                else:
                    pc += 1
            else:
                raise Exception("huh? {}".format(inst))


TEST_INPUT = """\
inc a
jio a, +2
tpl a
inc a
""".splitlines()

test_machine = Machine()
test_machine.run(parse_input(TEST_INPUT))
print("Test: register a is {}".format(test_machine.a))

machine = Machine()
machine.run(program)
print("Part 1: register b is {}".format(machine.b))

machine = Machine()
machine.a = 1
machine.run(program)
print("Part 2: register b is {}".format(machine.b))
