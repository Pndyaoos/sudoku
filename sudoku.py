"""
Module for solving Sudoku Puzzles
"""

class Cell(object):
    def __init__(self, index, value=None):
        self.index = index
        self.solved = False
        self.excludes = set()
        self.value = value if value is not None else " "
        self.groups = []

    def set_value(self, value, update_groups=True):
        """
        Set the value of this cell and update cells in parent boxes, rows
        and coulmuns
        """
        self.solved = True
        self.value = value
        self.excludes = set(range(1,10)).difference(set([value]))
        if update_groups:
            self.update_groups()

    def update_groups(self):
        for group in self.groups:
            group.update_excludes()

class Group(object):
    """
    A group of 9 values. Represents columns, rows and boxes.
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
        solved_cell = False
        for index, cell in enumerate(self.cells):
            others = [i for i in range(9) if i != index]
            for value in range(1,10):
                # If the cell is not already solved
                if not cell.solved:
                    # If this cell cannot hold this value, continue to next
                    # value
                    if value in cell.excludes:
                        continue
                    # If all other cells cannot hold this value, this cell
                    # must be this value. Break and go to next index
                    # print index, value, others, len(self.cells)
                    if all([value in self.cells[other].excludes for other in others]):
                        cell.set_value(value)
                        cell.update_groups()
                        solved_cell = True
                        break
        return solved_cell

    def update_excludes(self):
        """
        Update all the cells in this group based on the solved values
        """
        # collect solved values
        solved_values = set()
        for cell in self.cells:
            if cell.solved:
                solved_values.add(cell.value)

        # Update the cells with found values
        for cell in self.cells:
            cell.excludes.update(solved_values)

    def reference_group_to_cells(self):
        """
        Add a reference to this group for all the cells it contains
        """
        for cell in self.cells:
            cell.groups.append(self)

    def print_summary(self):
        for cell in self.cells:
            print "index: {0:2}, value: {1}, solved: {2!s:5}, excludes: {3}".format(
                cell.index, cell.value, cell.solved, cell.excludes)


class Grid(object):
    def __init__(self):
        self.cells = [Cell(index) for index in range(81)]
        self.rows = [Group(cells=self.cells[i*9:(i*9)+9]) for i in range(9)]
        self.columns = [Group(cells=self.cells[i:81:9]) for i in range(9)]
        self.boxes = [
            Group(cells=
                [self.cells[i], self.cells[i+1], self.cells[i+2],
                 self.cells[i+9], self.cells[i+10], self.cells[i+11],
                 self.cells[i+18], self.cells[i+19], self.cells[i+20]]
                 ) for i in [0,3,6,27,30,33,54,57,60]
            ]
        for row in self.rows:
            row.reference_group_to_cells()
        for column in self.columns:
            column.reference_group_to_cells()
        for box in self.boxes:
            box.reference_group_to_cells()

    def set_test_data(self):
        for i in range(81):
            self.cells[i].set_value(i, update_groups=False)

    def set_data_from_list(self, values):
        """
        Initiate all the cell values from a list
        """
        for index, value in enumerate(values):
            if value:
                self.cells[index].set_value(value, update_groups=False)

    def display(self):
        # for row in range(9):
        #     print "|".join(["{0:2}".format(self.cells[(row*9)+i].value) for i in range(9)])

        row_pattern = "|{0} {1} {2}|{3} {4} {5}|{6} {7} {8}|"
        seperator_pattern = "+-----+-----+-----+"

        print seperator_pattern
        print row_pattern.format(*[self.rows[0].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[1].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[2].cells[i].value for i in range(9)])
        print seperator_pattern
        print row_pattern.format(*[self.rows[3].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[4].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[5].cells[i].value for i in range(9)])
        print seperator_pattern
        print row_pattern.format(*[self.rows[6].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[7].cells[i].value for i in range(9)])
        print row_pattern.format(*[self.rows[8].cells[i].value for i in range(9)])
        print seperator_pattern

    def fill_excludes(self):
        for cell in self.cells:
            cell.update_groups()

    def solve(self, limit=None):
        solved_cell = True
        for _ in range(10):
            solved_cell = False
            for row in self.rows:
                solved_cell = row.solve() or solved_cell
            for column in self.columns:
                solved_cell = column.solve() or solved_cell
            for box in self.boxes:
                solved_cell = box.solve() or solved_cell
            print solved_cell


def experiments():

    easy_puzzle = [
        0, 2, 0,  1, 7, 8,  0, 3, 0,
        0, 4, 0,  3, 0, 2,  0, 9, 0,
        1, 0, 0,  0, 0, 0,  0, 0, 6,

        0, 0, 8,  6, 0, 3,  5, 0, 0,
        3, 0, 0,  0, 0, 0,  0, 0, 4,
        0, 0, 6,  7, 0, 9,  2, 0, 0,

        9, 0, 0,  0, 0, 0,  0, 0, 2,
        0, 8, 0,  9, 0, 1,  0, 6, 0,
        0, 1, 0,  4, 3, 6,  0, 5, 0
        ]

    grid = Grid()
    # grid.set_test_data()
    grid.set_data_from_list(easy_puzzle)
    grid.fill_excludes()

    # for row in grid.rows:
    #     print len(row.cells)
    # for column in grid.columns:
    #     print len(column.cells)
    # for box in grid.boxes:
    #     print len(box.cells)

    grid.display()

    # grid.boxes[5].print_summary()
    # grid.boxes[5].solve()
    # print ""
    # grid.boxes[5].print_summary()

    grid.solve()

    grid.display()

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
    # print grid.cells[42].groups[2].cells[3].value
    # print grid.cells[42].groups[0].cells[6].value
    # print grid.cells[42].groups[1].cells[4].value
    # grid.cells[42].groups[1].cells[4].value = -1
    # print grid.cells[42].value
    # print grid.rows[4].cells[6].value
    # print grid.columns[6].cells[4].value
    # print grid.boxes[5].cells[3].value
    # print grid.cells[42].groups[2].cells[3].value
    # print grid.cells[42].groups[0].cells[6].value
    # print grid.cells[42].groups[1].cells[4].value
    # grid.boxes[0].cells[0].value = " "

    # grid.display()

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