#!/usr/bin/env python3
# http://adventofcode.com/day/18
#
# Game of Life


def range2d(xlimit, ylimit):
    for x in range(xlimit):
        for y in range(ylimit):
            yield x, y

class Board:
    def __init__(self, rows, cols, cells=()):
        self.rows = rows
        self.cols = cols
        # cells is a set of pairs of ints.
        self.cells = set(cells)
        self.corners_stuck = False

    @classmethod
    def read_input(cls, inp):
        cells = set()
        for row, line in enumerate(inp):
            for col, char in enumerate(line.strip()):
                if char == "#":
                    cells.add((row, col))
        return cls(row+1, col+1, cells)

    def stick_corners(self, stuck):
        self.corners_stuck = stuck
        if stuck:
            self.cells.update([(0, 0), (self.rows-1, 0), (0, self.cols-1), (self.rows-1, self.cols-1)])

    def print(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print("#" if (row, col) in self.cells else ".", end="")
            print()

    def neighbors(self, row, col):
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            newrow = row + dr
            if 0 <= newrow < self.rows:
                newcol = col + dc
                if 0 <= newcol < self.cols:
                    yield newrow, newcol

    def next_board(self):
        next_gen = self.__class__(self.rows, self.cols)
        for row, col in range2d(self.rows, self.cols):
            n_neighbors = sum(nrc in self.cells for nrc in self.neighbors(row, col))
            if (row, col) in self.cells:
                # Cell is alive: needs 2 or 3 to live.
                if n_neighbors in (2, 3):
                    next_gen.cells.add((row, col))
            else:
                # Cell is dead: needs 3 to live.
                if n_neighbors == 3:
                    next_gen.cells.add((row, col))

        next_gen.stick_corners(self.corners_stuck)
        return next_gen

    def population(self):
        return len(self.cells)


def board_after_n(board, n_gen, show=False):
    if show:
        board.print()
    for _ in range(n_gen):
        board = board.next_board()
        if show:
            print("-" * 40)
            board.print()
    return board

TEST = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

test_board = Board.read_input(TEST.splitlines())
with open("day18_input.txt") as inp:
    input_board = Board.read_input(inp)

print("Part 1:")
end_state = board_after_n(test_board, 4, show=True)
print("Test: {} cells alive".format(end_state.population()))

end_state = board_after_n(input_board, 100)
print("Answer: {} cells alive".format(end_state.population()))

print("Part 2:")
test_board.stick_corners(True)
end_state = board_after_n(test_board, 5, show=True)
print("Test: {} cells alive".format(end_state.population()))

input_board.stick_corners(True)
end_state = board_after_n(input_board, 100)
print("Answer: {} cells alive".format(end_state.population()))
