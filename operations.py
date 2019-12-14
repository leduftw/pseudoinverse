"""This module contains utility functions which help in finding Moore-Penrose inverse"""

from sympy import *

__version__ = '1.0'


class Calculator:
    def __init__(self):
        pass

    def load_matrix(self, m, n):
        """
        Loads the matrix which user gives as input.
        """
        matrix = []
        for i in range(m):
            matrix.append(list(input().split()))
            if len(matrix[i]) != n:
                return None
        return matrix

    def calculate_general_1_inverse(self, matrix):
        pass

    def calculate_general_12_inverse(self, matrix):
        pass

    def calculate_general_13_inverse(self, matrix):
        pass

    def calculate_general_14_inverse(self, matrix):
        pass

    # REQUIRES FIX!
    def inverse(self, A):
        """
        Finds inverse of given square matrix A. The square matrix A has an inverse iff the det(A) != 0.
        If user gives matrix which is not square or if its determinant is zero, ValueError is thrown.
        """
        try:
            X = A ** -1
        except TypeError:
            return None
        return X

    def real_moore_penrose(self, A):
        """
        Utility function that calculates Moore-Penrose inverse of the given matrix A without any optimizations.
        See moore_penrose(A) for more details.
        """
        X = None
        return X

    def calculate_moore_penrose_inverse(self, matrix):
        """
        Returns Moore-Penrose inverse of given matrix A as well as information about regularity of matrix A.
        If the given matrix is regular this function will return tuple (inverse(A), True), otherwise
        it will return (real_moore_penrose(A), False).
        """
        try:
            X = self.inverse(matrix)
            regular = True
        except ValueError:
            X = self.real_moore_penrose(matrix)
            regular = False
        return X, regular
