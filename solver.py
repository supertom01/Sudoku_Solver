import numpy as np
import pandas as pd


def group_coordinate_to_row_coordinate(group: int, i: int) -> tuple[int, int]:
    """
    Translates the coordinate from a given group. To a coordinate in the sudoku itself.
    :param group: The group number (starting from 0 and till 9), counting from the top left to the right bottom.
    :param i:     The index of a number inside of that group (0-9), counting from the top left to the right bottom.
    :return:      The spatial coordinates in the sudoku itself (x,y)
    """
    return i // 3 + (group - (group % 3)), i % 3 + 3 * (group % 3)


class Sudoku(object):

    def __init__(self, field=None, filename=None):
        """
        A simple and naive sudoku solver. The solver can be used by either providing the field in a form of a two-
        dimensional list or by providing a filename to the constructor.

        The input of a sudoku is excepted as [[0, 1, 3, 0, 0, 0, 0, 8, 7], [...], [...]], when given as an array. If a
        filename is provided, the rows correspond with a single line and each number is separated by a space.

        :param field:    A two-dimensional array containing a sudoku representation.
        :param filename: A filepath to a sudoku representation.
        """
        if field is not None:
            self.field = field
        elif filename is not None:
            df = pd.read_csv(filename, header=None, sep=' ')
            self.field = np.array(df)
        else:
            raise RuntimeError('Either a field or filename is required in order to construct a Sudoku object.')

    @property
    def rows(self):
        """
        Get the rows of the sudoku.
        """
        return self.field

    @property
    def columns(self):
        """
        Get the columns of the sudoku.
        """
        return self.field.transpose()

    @property
    def groups(self):
        """
        Get the groups of the sudoku.
        """
        groups = np.zeros((9, 9))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        groups[j + 3 * k][i + 3 * l] = self.field[3 * k + l][i + 3 * j]
        return groups

    @property
    def valid(self) -> bool:
        """
        Checks if the sudoku is still valid.

        :return: True if the sudoku didn't violate any rules, otherwise False.
        """
        numbers = set(i for i in range(1, 10))
        for rows in [self.rows, self.columns, self.groups]:
            for row in rows:
                zeros = len(row) - np.count_nonzero(row)
                if len(numbers - set(row)) != zeros:
                    return False
        return True

    @property
    def filled(self) -> bool:
        """
        Checks if this sudoku is completely filled with numbers (doesn't have to be accurate!).

        :return: True if filled, otherwise False
        """
        return np.count_nonzero(self.field) == self.field.size

    def get_possible_values(self):
        """
        Retrieves for each index the possible numbers that can still fit according to the rules.
        :return: A two-dimensional array that contains a set for each position, with the numbers that can still fit.
        """
        numbers = set(i for i in range(1, 10))
        possible_values = [[numbers for _ in range(9)] for _ in range(9)]

        rows = self.rows
        for i in range(9):
            missing_numbers = numbers - set(rows[i])
            for j in range(9):
                if rows[i][j] == 0:
                    possible_values[i][j] = possible_values[i][j].intersection(missing_numbers)
                else:
                    possible_values[i][j] = set()  # Already filled, so no need to store numbers

        cols = self.columns
        for i in range(9):
            missing_numbers = numbers - set(cols[i])
            if len(missing_numbers) > 0:
                for j in range(9):
                    if cols[i][j] == 0:
                        possible_values[j][i] = possible_values[j][i].intersection(missing_numbers)

        groups = self.groups
        for i in range(9):
            missing_numbers = numbers - set(groups[i])
            if len(missing_numbers) > 0:
                for j in range(9):
                    if groups[i][j] == 0:
                        i2, j2 = group_coordinate_to_row_coordinate(i, j)
                        possible_values[i2][j2] = possible_values[i2][j2].intersection(missing_numbers)

        return possible_values

    def solve_single_position(self):
        """
        Attempts to solve a sudoku in a naive way.

        Checks for each cell the possible entries, if only one entry is possible fill it.
        Once it cannot find any more solutions the function is finished.

        This function can end in two ways:
        1. The sudoku is solved.
        2. There are only cells left with more than 1 valid entry.
        """
        old_fields = None
        while old_fields is None or not np.array_equal(old_fields, self.field):
            old_fields = np.copy(self.field)

            # Infer all possible options in empty locations
            possible_values = self.get_possible_values()

            # If a location has a single option, fill it
            values_added = 0
            shortest_length = 10
            for i in range(9):
                for j in range(9):
                    length = len(possible_values[i][j])
                    if length == 1 and self.field[i][j] == 0:
                        self.field[i][j] = possible_values[i][j].pop()
                        values_added += 1
                    if length < shortest_length:
                        shortest_length = length

    def solve(self):
        """
        Solves the sudoku in an iterative way.

        First we fill all the values that can immediately be filled in, by just checking that only one value is valid
        on a given index. Next we start guessing possible options till we have reached a fully filled and valid sudoku.
        """
        self.solve_single_position()
        if not self.filled:

            # Find the shortest possible option
            possible_values = self.get_possible_values()

            min_possible_options = min(min((len(possible_values[i][j]) for j in range(9) if len(possible_values[i][j]) > 0), default=20) for i in range(9))
            if min_possible_options == 20:
                return

            # Search for the shortest option
            x = None
            y = None
            for i in range(9):
                for j in range(9):
                    length = len(possible_values[i][j])
                    if length == min_possible_options:
                        x = i
                        y = j
                        break
                if x is not None:
                    break

            # Try to solve the sudoku for each possible option
            for i in range(min_possible_options):
                sudoku_copy = Sudoku(np.copy(self.field))
                sudoku_copy.field[x][y] = possible_values[x][y].pop()
                sudoku_copy.solve()
                if sudoku_copy.filled and sudoku_copy.valid:
                    self.field = sudoku_copy.field
                    return

    def __str__(self):
        str = ''
        for row in self.field:
            for val in row:
                str += f'{val:2.0f} '
            str += '\r\n'
        return str