"""
Module for solving Sudoku Puzzles
"""

from itertools import combinations

class Cell(object):
    def __init__(self, index, value=None):
        self.index = index
        self.solved = False
        self.excludes = set()
        self.candidates = set(range(1,10))
        self.value = value if value is not None else " "
        self.box = None
        self.column = None
        self.row = None
        self.dirty = False

    def set_value(self, value, update_siblings=True):
        """
        Set the value of this cell and update cells in parent boxes, rows
        and coulmuns
        """
        print "Solved {0} as {1}".format(self.index, value)
        self.solved = True
        self.value = value
        self.excludes = set(range(1,10)).difference(set([value]))
        self.candidates = set([value])
        self.dirty = True
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
        # print self.excludes, excluded_vals
        # print not excluded_vals.issubset(self.excludes)
        if not self.solved and not excluded_vals.issubset(self.excludes):
            self.excludes.update(excluded_vals)
            self.candidates = set(range(1,10)).difference(self.excludes)
            self.dirty = True

    def trivial_solve(self):
        if (len(self.candidates) == 1) and (not self.solved):
            self.set_value(list(self.candidates)[0])

    def get_summary(self):
        return "in: {0:2}, va: {1}, so: {2!s:5}, exc: {3}".format(
            self.index, self.value, self.solved, self.excludes)

class Group(object):
    """
    A group of 9 values.
    """
    def __init__(self, cells=None):
        self.cells = cells if cells is not None else []

    def get_unsolved_values(self):
        """
        Get the set of values that still need to be solved for this group
        """
        return set(range(1,10)).difference(self.get_solved_values())

    def get_solved_values(self):
        """
        Get the set of values that have been solved for this group
        """
        return set([cell.value for cell in self.get_solved_cells()])

    def get_unsolved_cells(self):
        """
        Get the unsolved cells in this group
        """
        return [cell for cell in self.cells if not cell.solved]

    def get_solved_cells(self):
        """
        Get the solved cells in this group
        """
        return [cell for cell in self.cells if cell.solved]

    def update_excludes(self):
        """
        Update all the cells in this group based on the solved values
        """
        for cell in self.cells:
            cell.add_excludes(self.get_solved_values())

    def print_summary(self):
        for cell in self.cells:
            print cell.get_summary()

    def exclusion_solve(self):
        """
        Look for cells in this group that must have a certain value

        For all the unsolved cells in the group, go over each value and
        if the value can go in that cell, and cannot go in all other
        cells then that cell must contain that value
        """
        for cell in self.get_unsolved_cells():
            for value in self.get_unsolved_values():
                # If this cell cannot hold this value, continue to next
                # value
                if value in cell.excludes:
                    continue
                # If all other cells cannot hold this value, this cell
                # must be this value. Break and go to next index
                if all([value in other.excludes for other in self.cells if other is not cell]):
                    cell.set_value(value)
                    break

    def naked_pair_exclude(self):
        """
        If two unsolved cells both have exactly 2 candidates and those
        candidate pairs are the same, then all other unsolved cells in
        this group cannot have those values as candidates

        http://www.sudokuwiki.org/Naked_Candidates
        """

        pair_pool = [cell for cell in self.get_unsolved_cells() if
            len(cell.candidates) == 2]
        if len(pair_pool) >= 2:
            for a, b in combinations(pair_pool, 2):
                if a.candidates == b.candidates:
                    for cell in self.get_unsolved_cells():
                        if (cell is not a) and (cell is not b):
                            print "pair exclude: {0} and {1}".format(a.index, b.index)
                            cell.add_excludes(a.candidates)

    def naked_triple_exclude(self):
        """
        http://www.sudokuwiki.org/Naked_Candidates
        
        If the union of candidates of 3 unsolved cells is of size 3 then
        all other unsolved cells cannot have any of the elements of this union
        as candidates
        """

        triple_pool = self.get_unsolved_cells()
        if len(triple_pool) >= 3:
            for a, b, c in combinations(triple_pool, 3):
                union = a.candidates.union(b.candidates.union(c.candidates))
                if len(union) == 3:
                    for cell in self.get_unsolved_cells():
                        if (cell is not a) and (cell is not b) and (cell is not c):
                            print "Triple exclude: {0} and {1} and {2}".format(a.index, b.index, c.index)
                            cell.add_excludes(union)


    # def naked_subset(self):
    #     pass
    #     http://www.sudokuwiki.org/Naked_Candidates
    #     for cell in unsolved cells:
    #         n = number of candidates for this cell
    #         matches = 1
    #         for other in other_unsloved:
    #             if other.candidate_set == cell.candidate_set:
    #                 matches +=1
    #         # if exactly n cells (including this cell) have the same candidate set in this group: ()
    #         if matches == n:

    #         if exactly n cells (including this cell) have the same candidate set in this group: ()
    #             (remove the candidates from) / (add candidates to excludes) the other unsolved cells



    #     u = number of unsolved cells
    #     if u < 2:
    #         return
    #     for s in range(2,u+1)


class Box(Group):
    """
    A 3x3 set of cells
    """
    def reference_group_to_cells(self):
        """
        Add a reference to this box for all the cells it contains
        """
        for cell in self.cells:
            cell.box = self

    def single_line_exclusion(self):
        # If all unsolved cells in this box are in a single line
        #   unsolved cells in that line not in this box cannot be any of the unsolved values in this box - otherwise the value couldnt be in this box
        #   add unsolved values to excludes of other cells in that line

        unsolved_cells = self.get_unsolved_cells()
        if len(unsolved_cells) in [2,3]:
            first = unsolved_cells[0]
            line = None
            if all(cell.row is first.row for cell in unsolved_cells[1:]):
                line = first.row
            if line is None:
                if all(cell.column is first.column for cell in unsolved_cells[1:]):
                    line = first.column
            if line is not None:
                for cell in [cell for cell in line.cells if cell.box is not self]:
                    cell.add_excludes(self.get_unsolved_values())


class Line(Group):
    """
    9 cells in a line
    """
    def single_box_exclude(self):
    #     # If the unsolved 2 or 3 cells in this line are in a single box:
    #     # Add the candidate values to the excludes of the other cells in the box/
        pass

class Row(Line):
    """
    A horizontal line of cells
    """
    def reference_group_to_cells(self):
        """
        Add a reference to this row for all the cells it contains
        """
        for cell in self.cells:
            cell.row = self

class Column(Line):
    """
    A vertical line of cells
    """
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
        self.groups = self.columns + self.rows + self.boxes
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
        for group in self.groups:
            group.update_excludes()

    def solve(self, limit=5):
        state_updated = True
        runs = 0
        while runs < limit and self.any_dirty_cells():
            print runs
            self.clean_all_cells()
            runs += 1
            for cell in self.cells:
                cell.trivial_solve()
            for group in self.groups:
                group.exclusion_solve()
                group.naked_pair_exclude()
                group.naked_triple_exclude()
            for box in self.boxes:
                box.single_line_exclusion()

    def any_dirty_cells(self):
        for cell in self.cells:
            if cell.dirty:
                return True
        return False

    def clean_all_cells(self):
        for cell in self.cells:
            cell.dirty = False


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

    triple_test = [
        2, 9, 4,  5, 1, 3,  0, 0, 6,
        6, 0, 0,  8, 4, 2,  3, 1, 9,
        3, 0, 0,  6, 9, 7,  2, 5, 4,

        0, 0, 0,  0, 5, 6,  0, 0, 0,
        0, 4, 0,  0, 8, 0,  0, 6, 0,
        0, 0, 0,  4, 7, 0,  0, 0, 0,

        7, 3, 0,  1, 6, 4,  0, 0, 5,
        9, 0, 0,  7, 3, 5,  0, 0, 1,
        4, 0, 0,  9, 2, 8,  6, 3, 7
        ]


    grid = Grid()
    # grid.set_test_data()
    grid.set_data_from_list(hard_puzzle)
    grid.print_summary()

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

        # every box intersects 3 rows and 3 columns
        # every row intersects 3 boxes and 9 columns
        # every column intersects 3 boxes and 9 rows
        # every cell is in one box, row and column