import unittest

import numpy as np

from solver import Sudoku, group_coordinate_to_row_coordinate


class TestStaticFunctions(unittest.TestCase):

    def test_translate_coordinate(self):
        self.assertEqual((1, 0), group_coordinate_to_row_coordinate(0, 3))
        self.assertEqual((2, 8), group_coordinate_to_row_coordinate(2, 8))
        self.assertEqual((3, 3), group_coordinate_to_row_coordinate(4, 0))
        self.assertEqual((7, 1), group_coordinate_to_row_coordinate(6, 4))


class TestSudoku(unittest.TestCase):
    INIT_FIELD = np.array([
        [8, 0, 0, 0, 1, 0, 6, 0, 9],
        [0, 0, 1, 9, 7, 0, 0, 2, 0],
        [9, 4, 0, 8, 2, 6, 3, 0, 1],
        [0, 0, 4, 6, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 1, 6, 0],
        [5, 0, 6, 0, 3, 2, 9, 8, 0],
        [4, 0, 0, 0, 5, 8, 7, 1, 0],
        [6, 2, 0, 1, 0, 0, 5, 3, 0],
        [0, 5, 8, 0, 0, 7, 4, 0, 2]
    ])
    INIT_FIELD_COLUMNS = np.array([
        [8, 0, 9, 0, 0, 5, 4, 6, 0],
        [0, 0, 4, 0, 9, 0, 0, 2, 5],
        [0, 1, 0, 4, 0, 6, 0, 0, 8],
        [0, 9, 8, 6, 0, 0, 0, 1, 0],
        [1, 7, 2, 0, 0, 3, 5, 0, 0],
        [0, 0, 6, 0, 0, 2, 8, 0, 7],
        [6, 0, 3, 0, 1, 9, 7, 5, 4],
        [0, 2, 0, 0, 6, 8, 1, 3, 0],
        [9, 0, 1, 0, 0, 0, 0, 0, 2]
    ])
    INIT_FIELD_GROUPS = np.array([
        [8, 0, 0, 0, 0, 1, 9, 4, 0],
        [0, 1, 0, 9, 7, 0, 8, 2, 6],
        [6, 0, 9, 0, 2, 0, 3, 0, 1],
        [0, 0, 4, 0, 9, 0, 5, 0, 6],
        [6, 0, 0, 0, 0, 0, 0, 3, 2],
        [0, 0, 0, 1, 6, 0, 9, 8, 0],
        [4, 0, 0, 6, 2, 0, 0, 5, 8],
        [0, 5, 8, 1, 0, 0, 0, 0, 7],
        [7, 1, 0, 5, 3, 0, 4, 0, 2]
    ])

    def test_rows(self):
        sudoku = Sudoku(self.INIT_FIELD)
        np.testing.assert_array_equal(sudoku.field, sudoku.rows)

        sudoku = Sudoku(self.INIT_FIELD_COLUMNS)
        np.testing.assert_array_equal(sudoku.field, sudoku.rows)

    def test_columns(self):
        sudoku = Sudoku(self.INIT_FIELD)
        np.testing.assert_array_equal(self.INIT_FIELD_COLUMNS, sudoku.columns)

        sudoku = Sudoku(self.INIT_FIELD_COLUMNS)
        np.testing.assert_array_equal(self.INIT_FIELD, sudoku.columns)

    def test_groups(self):
        sudoku = Sudoku(self.INIT_FIELD)
        np.testing.assert_array_equal(self.INIT_FIELD_GROUPS, sudoku.groups)

    def test_valid(self):
        sudoku = Sudoku(self.INIT_FIELD)
        self.assertTrue(sudoku.valid)
        sudoku = Sudoku(self.INIT_FIELD_COLUMNS)
        self.assertTrue(sudoku.valid)

    def test_solve(self):
        sudoku = Sudoku(self.INIT_FIELD)
        print(sudoku)
        sudoku.solve_single_position()
        self.assertTrue(sudoku.valid)
        print(sudoku)
