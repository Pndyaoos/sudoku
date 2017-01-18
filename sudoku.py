"""
Module for solving Sudoku Puzzles
"""

class Cell(object):
    def __init__(self, index, value=None):
        self.index = index
        self.solved = False
        self.excludes = set()
        self.value = value if value is not None else " "
        self.box = None
        self.column = None
        self.row = None

    def set_value(self, value, update_siblings=True):
        """
        Set the value of this cell and update cells in parent boxes, rows
        and coulmuns
        """
        self.solved = True
        self.value = value
        self.excludes = set(range(1,10)).difference(set([value]))
        if update_siblings:
            self.update_siblings()

    def update_siblings(self):
            self.box.update_excludes()
            self.column.update_excludes()
            self.row.update_excludes()

    def add_excludes(self, excluded_vals):
        """
        Update the values that this cell cannot be, must be a set
        """

        if self.solved:
            return
        else:
            self.excludes.update(excluded_vals)

    def trivial_solve(self):
        if (len(self.excludes) == 8) and (not self.solved):
            self.value = set(range(1,10)).difference(self.excludes).pop()
            self.solved = True
            self.update_siblings()
            print "Solved {0} as {1}".format(self.index, self.value)
            return True
        else:
            return False

    def get_summary(self):
        return "in: {0:2}, va: {1}, so: {2!s:5}, exc: {3}".format(
            self.index, self.value, self.solved, self.excludes)

class Group(object):
    """
    A group of 9 values. Base class for columns, rows and boxes.
    """
    def __init__(self, cells=None):
        self.cells = cells if cells is not None else []

    def exclusion_solve(self):
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
                        cell.update_siblings()
                        solved_cell = True
                        print "Solved {0} as {1}".format(cell.index, value)
                        break
        return solved_cell

        # every box intersects 3 rows and 3 columns
        # every row intersects 3 boxes and 9 columns
        # every column intersects 3 boxes and 9 rows
        # every cell is in one box, row and column

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
            cell.add_excludes(solved_values)

    def print_summary(self):
        for cell in self.cells:
            print cell.get_summary()

class Box(Group):
    def reference_group_to_cells(self):
        """
        Add a reference to this box for all the cells it contains
        """
        for cell in self.cells:
            cell.box = self

    def single_line_exclusion(self):
        # for unsolved values in box:
        #     if all possible cells for current value are in a single row/column:
        #         cells in that row/column not in this box cannot hold current value, otherwise the value couldnt be in this box
        #         add current value to the excludes of those cells

        state_changed = False
        for value in set(range(1,10)).difference(set([cell.value for cell in self.cells if cell.solved])):
            available_cells = [cell for cell in self.cells if (value not in cell.excludes) and (not cell.solved)]
            if len(available_cells) > 1:
                line = None
                row = available_cells[0].row
                if all([cell.row is row for cell in available_cells[1:]]):
                    line = row
                if line is None:
                    column = available_cells[0].column
                    if all([cell.column is column for cell in available_cells[1:]]):
                        line = column
                if line is None:
                    continue
                else:
                    for cell in [cell for cell in line.cells if cell.box is not self]:
                        cell.add_excludes(set([value]))
                        state_changed = True
        return state_changed


class Row(Group):
    def reference_group_to_cells(self):
        """
        Add a reference to this row for all the cells it contains
        """
        for cell in self.cells:
            cell.row = self

class Column(Group):
    def reference_group_to_cells(self):
        """
        Add a reference to this column for all the cells it contains
        """
        for cell in self.cells:
            cell.column = self

class Grid(object):
    def __init__(self):
        self.cells = [Cell(index) for index in range(81)]
        self.rows = [Row(cells=self.cells[i*9:(i*9)+9]) for i in range(9)]
        self.columns = [Column(cells=self.cells[i:81:9]) for i in range(9)]
        self.boxes = [
            Box(cells=
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
            self.cells[i].set_value(i, update_siblings=False)

    def set_data_from_list(self, values):
        """
        Initiate all the cell values from a list
        """
        for index, value in enumerate(values):
            if value:
                self.cells[index].set_value(value, update_siblings=False)

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

    def print_summary(self):
        for row in range(9):
            if row %3 == 0:
                print "-"
            print "{0:65}{1:65}{2}".format(
                self.cells[row*9].get_summary(),
                self.cells[row*9 + 3].get_summary(),
                self.cells[row*9 + 6].get_summary())
            print "{0:65}{1:65}{2}".format(
                self.cells[row*9 + 1].get_summary(),
                self.cells[row*9 + 4].get_summary(),
                self.cells[row*9 + 7].get_summary())
            print "{0:65}{1:65}{2}".format(
                self.cells[row*9 + 2].get_summary(),
                self.cells[row*9 + 5].get_summary(),
                self.cells[row*9 + 8].get_summary())

    def fill_excludes(self):
        for cell in self.cells:
            cell.update_siblings()

    def solve(self, limit=5):
        state_updated = True
        runs = 0
        while state_updated and runs < limit:
            state_updated = False
            runs += 1
            for cell in self.cells:
                state_updated = cell.trivial_solve() or state_updated
            for row in self.rows:
                state_updated = row.exclusion_solve() or state_updated
            for column in self.columns:
                state_updated = column.exclusion_solve() or state_updated
            for box in self.boxes:
                state_updated = box.exclusion_solve() or state_updated
                state_updated = box.single_line_exclusion() or state_updated
            print state_updated


def experiments():

    empty = [
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,

        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,

        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0
        ]

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

    hard_puzzle = [
        0, 0, 4,  3, 0, 0,  6, 2, 0,
        0, 0, 7,  0, 0, 0,  0, 0, 9,
        0, 0, 9,  0, 2, 0,  8, 5, 0,

        0, 1, 0,  0, 5, 0,  0, 0, 0,
        4, 0, 0,  8, 0, 1,  0, 0, 2,
        0, 0, 0,  0, 3, 0,  0, 6, 0,

        0, 4, 6,  0, 1, 0,  7, 0, 0,
        9, 0, 0,  0, 0, 0,  2, 0, 0,
        0, 8, 1,  0, 0, 2,  3, 0, 0
        ]

    line_excl_test = [
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,

        0, 0, 0,  0, 0, 0,  1, 0, 2,
        7, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  3, 0, 4,

        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0,
        0, 0, 0,  0, 0, 0,  0, 0, 0
        ]

    grid = Grid()
    # grid.set_test_data()
    grid.set_data_from_list(hard_puzzle)
    grid.fill_excludes()


    # for row in grid.rows:
    #     print len(row.cells)
    # for column in grid.columns:
    #     print len(column.cells)
    # for box in grid.boxes:
    #     print len(box.cells)

    grid.display()
    grid.solve()
    grid.display()
    
    grid.print_summary()

    # grid.boxes[5].print_summary()
    # grid.boxes[5].solve()
    # print ""
    # grid.boxes[5].print_summary()
    # grid.boxes[2].print_summary()
    # print "-"
    # grid.boxes[4].print_summary()
    # print "-"
    # grid.boxes[8].print_summary()

    # grid.boxes[5].single_line_exclusion()

    # grid.display()
    # print "-"
    # grid.boxes[2].print_summary()
    # print "-"
    # grid.boxes[4].print_summary()
    # print "-"
    # grid.boxes[8].print_summary()
    # grid.rows[0].print_summary()

experiments()


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