"""
Module for solving Sudoku Puzzles
"""

class Cell(object):
    def __init__(self, value=None):
        self.solved = False
        self.excludes = set()
        self.value = value if value is not None else -1
        self.row = None
        self.column = None
        self.box = None

    def exclude(self):
        # add all values in parent row, column and box to the excluded set
        pass

    def set_value(self, value, update_parents=True):
        """
        Set the value of this cell and update cells in parent boxes, rows
        and coulmuns
        """

        self.solved = True
        self.value = value
        if update_parents:
            self.update_parents()

    def update_parents(self):
        self.row.update_excludes()
        self.column.update_excludes()
        self.box.update_excludes()

class Group(object):
    """
    A group of 9 values, this could be a box or a line
    """
    def __init__(self, cells=None):
        self.cells = cells if cells is not None else []

    def solve(self):
        """
        Look for cells in this group that must have a certain value

        For all the unsolved cells in the group, go over each value and
        if the value can go in that cell, and cannot go in all other
        cells then that cell must contain that value
        """

        for index in range(9):
            others = [i for i in range(9) if i != index]
            for value in range(1,10):
                # If the cell is not already solved
                if not self.cells[index].solved:
                    # If this cell cannot hold this value, continue to next
                    # value
                    if value in self.cells[index].excludes:
                        continue
                    # If all other cells cannot hold this value, this cell
                    # must be this value. Break and go to next index
                    if all([value in self.cells[other].excludes
                            for other in others]):
                        self.cells[index].set_value(value)
                        break

    def update_excludes(self):
        """
        Update all the cells in this group based on the solved values
        """

        # collect solved values
        solved_values = set()
        for index in range(9):
            cell = self.cells[index]
            if cell.solved:
                solved_values.add(cell.value)

        # Update the cells with found values
        for index in range(9):
            self.cells[index].excludes.update(solved_values)


class Grid(object):
    def __init__(self):
        self.cells = [Cell() for _ in range(81)]
        self.rows = [Group(cells=self.cells[i*9:(i*9)+8]) for i in range(9)]
        self.columns = [Group(cells=self.cells[i:81:9]) for i in range(9)]
        self.boxes = [
            Group(cells=
                [self.cells[i], self.cells[i+1], self.cells[i+2],
                 self.cells[i+9], self.cells[i+10], self.cells[i+11],
                 self.cells[i+18], self.cells[i+19], self.cells[i+20]]
                 ) for i in [0,3,6,27,30,33,54,57,60]
            ]


    def set_test_data(self):
        for i in range(81):
            self.cells[i].set_value(i, update_parents=False)


    def display(self):
        for row in range(9):
            print "|".join(["{0:2}".format(self.cells[(row*9)+i].value) for i in range(9)])


def experiments():
    grid = Grid()
    grid.set_test_data()

    print grid.cells[0].value
    print grid.rows[0].cells[0].value
    print grid.columns[0].cells[0].value
    print grid.boxes[0].cells[0].value

    grid.cells[0].value = 99

    print grid.cells[0].value
    print grid.rows[0].cells[0].value
    print grid.columns[0].cells[0].value
    print grid.boxes[0].cells[0].value

    grid.columns[0].cells[0].value = 999

    print grid.cells[0].value
    print grid.rows[0].cells[0].value
    print grid.columns[0].cells[0].value
    print grid.boxes[0].cells[0].value

    print grid.cells[42].value
    print grid.rows[4].cells[6].value
    print grid.columns[6].cells[4].value
    print grid.boxes[5].cells[3].value

    grid.boxes[0].cells[0].value = 0

    grid.display()

    # unsolved_cell_indices = [1,2,3]
    # unsolved_values = [4,5,6]

    # for index in unsolved_cell_indices:
    #     for value in unsolved_values[:]:
    #         print unsolved_values
    #         if index == 2:
    #             if 5 in unsolved_values:
    #                 unsolved_values.remove(5)

experiments()

        # self.cell_to_noncolumn = {
        #     0: [1,2],
        #     3: [1,2],
        #     6: [1,2],
        #     1: [0,2],
        #     4: [0,2],
        #     7: [0,2],
        #     2: [0,1],
        #     5: [0,1],
        #     8: [0,1]
        #     }
        # self.cell_to_nonrow = {
        #     0: [1,2],
        #     1: [1,2],
        #     2: [1,2],
        #     3: [0,2],
        #     4: [0,2],
        #     5: [0,2],
        #     6: [0,1],
        #     7: [0,1],
        #     8: [0,1]
        #     }