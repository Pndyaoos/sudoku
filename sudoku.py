"""
Module for solving Sudoku Puzzles
"""

class Cell(object):
    def __init__(self, value=None):
        self.solved = False
        self.excluded = []
        self.value = value if value is not None else -1
        self.row = None
        self.column = None
        self.box = None

    def exclude(self):
        # add all values in parent row, column and box to the excluded set
        pass


class Line(object):
    def __init__(self, cells=None):
        self.cells = cells if cells is not None else []


class Box(object):
    def __init__(self, cells=None):
        self.cells = cells if cells is not None else []
        self.rows = []
        self.columns = []
        self.unsolved_cell_indices = []
        self.unsolved_values = []
        self.cell_to_noncolumn = {
            0: [1,2],
            3: [1,2],
            6: [1,2],
            1: [0,2],
            4: [0,2],
            7: [0,2],
            2: [0,1],
            5: [0,1],
            8: [0,1]
            }
        self.cell_to_nonrow = {
            0: [1,2],
            1: [1,2],
            2: [1,2],
            3: [0,2],
            4: [0,2],
            5: [0,2],
            6: [0,1],
            7: [0,1],
            8: [0,1]
            }

    def eliminate(self):
        """
        Look for cells that must have a certain value
        For all the unsolved cell in


        """

        for index in range(9):
            others = range(9)
            others.remove(index)
            for value in range(1,10):
                # If the cell is not already solved
                if not self.cells[index].solved:
                    # If this cell cannot hold this value, continue to next value
                    if value not in self.cells[index].possible_values
                        continue

                    # If all other cells cannot hold this value, this cell must be this value. Break and go to next value
                    if all([value not in self.cells[other].possible_values for other in others]):
                        self.cells[index].set_solved(value)
                        break

class Grid(object):
    def __init__(self):
        self.cells = []
        self.rows = []
        self.columns = []

    def setuptest(self):
        self.cells = [Cell(value=i) for i in range(81)]

        self.rows = [Line(cells=self.cells[i*9:(i*9)+8]) for i in range(0,9)]

        self.columns = [
            Line(cells=[self.cells[i] for i in range(0,81,9)]),
            Line(cells=[self.cells[i] for i in range(1,81,9)]),
            Line(cells=[self.cells[i] for i in range(2,81,9)]),
            Line(cells=[self.cells[i] for i in range(3,81,9)]),
            Line(cells=[self.cells[i] for i in range(4,81,9)]),
            Line(cells=[self.cells[i] for i in range(5,81,9)]),
            Line(cells=[self.cells[i] for i in range(6,81,9)]),
            Line(cells=[self.cells[i] for i in range(7,81,9)]),
            Line(cells=[self.cells[i] for i in range(8,81,9)])
            ]

        self.boxes = [
            Box(cells=
                [self.cells[i], self.cells[i+1], self.cells[i+2],
                 self.cells[i+9], self.cells[i+10], self.cells[i+11],
                 self.cells[i+18], self.cells[i+19], self.cells[i+20]]
                 ) for i in [0,3,6,27,30,33,54,57,60]
            ]

    def display(self):
        for row in range(9):
            print "|".join(["{0:2}".format(self.cells[(row*9)+i].value) for i in range(9)])


def experiments():
    # grid = Grid()
    # grid.setuptest()

    # print grid.cells[0].value
    # print grid.rows[0].cells[0].value
    # print grid.columns[0].cells[0].value
    # print grid.boxes[0].cells[0].value

    # grid.cells[0].value = 99

    # print grid.cells[0].value
    # print grid.rows[0].cells[0].value
    # print grid.columns[0].cells[0].value
    # print grid.boxes[0].cells[0].value

    # grid.columns[0].cells[0].value = 999

    # print grid.cells[0].value
    # print grid.rows[0].cells[0].value
    # print grid.columns[0].cells[0].value
    # print grid.boxes[0].cells[0].value

    # print grid.cells[42].value
    # print grid.rows[4].cells[6].value
    # print grid.columns[6].cells[4].value
    # print grid.boxes[5].cells[3].value

    # grid.boxes[0].cells[0].value = 0

    # grid.display()

    unsolved_cell_indices = [1,2,3]
    unsolved_values = [4,5,6]

    for index in unsolved_cell_indices:
        for value in unsolved_values[:]:
            print unsolved_values
            if index == 2:
                if 5 in unsolved_values:
                    unsolved_values.remove(5)

experiments()