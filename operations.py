"""Module for calculating pseudoinverses"""

from sympy import *

__version__ = '1.0'


class Calculator:
    def __init__(self):
        # Matrices
        self.P = None
        self.Q = None

    @staticmethod
    def load_matrix(m, n):
        """
        Loads the matrix which user gives as input.
        """
        matrix = []
        for i in range(m):
            matrix.append(list(input().split()))
            if len(matrix[i]) != n:
                return None
        return matrix

    def calculate_P_Q(self, matrix):
        if matrix is None:
            self.P = None
            self.Q = None
            return
        m, n = matrix.shape
        # print(m, n)
        extended_user_matrix = matrix.row_join(eye(m))
        # pprint(extended_user_matrix)
        extended_user_matrix = extended_user_matrix.rref(simplify=True, pivots=False)
        print('Resena prvo:')
        pprint(extended_user_matrix)
        print()
        # pprint(extended_user_matrix)
        self.P = extended_user_matrix[:m, n:]
        print('P')
        pprint(self.P)
        print()
        extended_user_matrix = extended_user_matrix[:m, :n]
        extended_user_matrix = extended_user_matrix.col_join(eye(n))
        print('Dodato In')
        pprint(extended_user_matrix)
        print()
        extended_user_matrix = extended_user_matrix.transpose()
        extended_user_matrix = extended_user_matrix.rref(simplify=True, pivots=False)
        print("Reseno")
        pprint(extended_user_matrix)
        print()
        extended_user_matrix = extended_user_matrix.transpose()
        print("Transponovano")
        pprint(extended_user_matrix)
        print()
        print('Dimenzije: ', extended_user_matrix.shape)
        print('m, n:', m, n)
        self.Q = extended_user_matrix[m:, :n]
        print('Q')
        pprint(self.Q)
        print()

        # Nakon ove tacke u self.P i self.Q se nalaze matrice P i Q

    def calculate_general_1_inverse(self, matrix):
        self.calculate_P_Q(matrix)
        m, n = matrix.shape
        r = matrix.rank()
        hasX1 = m - r > 0
        hasX2 = n - r > 0
        hasX3 = hasX1 and hasX2

        X0 = MatrixSymbol('X0', r, r)
        X1 = MatrixSymbol('X1', r, m - r)
        X2 = MatrixSymbol('X2', n - r, r)
        X3 = MatrixSymbol('X3', n - r, m - r)

        if hasX3:
            Xu = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            Xu = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            Xu = BlockMatrix(2, 1, [X0, X2])
        else:
            Xu = BlockMatrix(1, 1, [X0])
        Xu = Xu.subs(X0, eye(r))
        pprint(Xu)

    def calculate_general_12_inverse(self, matrix):
        self.calculate_P_Q(matrix)
        m, n = matrix.shape
        r = matrix.rank()
        hasX1 = m - r > 0
        hasX2 = n - r > 0
        hasX3 = hasX1 and hasX2

        X0 = MatrixSymbol('X0', r, r)
        X1 = MatrixSymbol('X1', r, m - r)
        X2 = MatrixSymbol('X2', n - r, r)
        X3 = MatrixSymbol('X3', n - r, m - r)

        if hasX3:
            Xu = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            Xu = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            Xu = BlockMatrix(2, 1, [X0, X2])
        else:
            Xu = BlockMatrix(1, 1, [X0])

        Xu = Xu.subs(X0, eye(r))
        if hasX3:
            Xu = Xu.subs(X3, X2 * X1)
        pprint(Xu)

    def calculate_general_13_inverse(self, matrix):
        self.calculate_P_Q(matrix)
        m, n = matrix.shape
        r = matrix.rank()
        hasX1 = m - r > 0
        hasX2 = n - r > 0
        hasX3 = hasX1 and hasX2

        X0 = MatrixSymbol('X0', r, r)
        X1 = MatrixSymbol('X1', r, m - r)
        X2 = MatrixSymbol('X2', n - r, r)
        X3 = MatrixSymbol('X3', n - r, m - r)

        # Shapes
        # S  -> (m, m)
        # S1 -> (r, r)
        # S2 -> (r, m - r)
        # S3 -> (m - r, r)
        # S4 -> (m - r, m - r)
        S = self.P * self.P.transpose()

        # X1 = -S2 * S4 ** -1, it is guaranteed that S4 has inverse
        S2 = S[:r, r:]
        S4 = S[r:, r:]

        if hasX3:
            Xu = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            Xu = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            Xu = BlockMatrix(2, 1, [X0, X2])
        else:
            Xu = BlockMatrix(1, 1, [X0])

        Xu = Xu.subs(X0, eye(r))
        if hasX3 or hasX1:
            Xu = Xu.subs(X1, -S2 * S4 ** -1)
        pprint(Xu)

    def calculate_general_14_inverse(self, matrix):
        self.calculate_P_Q(matrix)
        m, n = matrix.shape
        r = matrix.rank()
        hasX1 = m - r > 0
        hasX2 = n - r > 0
        hasX3 = hasX1 and hasX2

        X0 = MatrixSymbol('X0', r, r)
        X1 = MatrixSymbol('X1', r, m - r)
        X2 = MatrixSymbol('X2', n - r, r)
        X3 = MatrixSymbol('X3', n - r, m - r)

        # Shapes
        # T  -> (n, n)
        # T1 -> (r, r)
        # T2 -> (r, n - r)
        # T3 -> (n - r, r)
        # T4 -> (n - r, n - r)
        T = self.Q.transpose() * self.Q

        # X2 = -T4 ** -1 * T3, it is guaranteed that T4 has inverse
        T3 = T[r:, :r]
        T4 = T[r:, r:]

        if hasX3:
            Xu = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            Xu = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            Xu = BlockMatrix(2, 1, [X0, X2])
        else:
            Xu = BlockMatrix(1, 1, [X0])

        Xu = Xu.subs(X0, eye(r))
        if hasX3 or hasX2:
            Xu = Xu.subs(X2, -T4 ** -1 * T3)
        pprint(Xu)

    def calculate_moore_penrose_inverse(self, matrix):
        self.calculate_P_Q(matrix)
        m, n = matrix.shape
        r = matrix.rank()
        hasX1 = m - r > 0
        hasX2 = n - r > 0
        hasX3 = hasX1 and hasX2

        X0 = MatrixSymbol('X0', r, r)
        X1 = MatrixSymbol('X1', r, m - r)
        X2 = MatrixSymbol('X2', n - r, r)
        X3 = MatrixSymbol('X3', n - r, m - r)

        # Shapes
        #
        # S  -> (m, m)
        # S1 -> (r, r)
        # S2 -> (r, m - r)
        # S3 -> (m - r, r)
        # S4 -> (m - r, m - r)
        #
        # T  -> (n, n)
        # T1 -> (r, r)
        # T2 -> (r, n - r)
        # T3 -> (n - r, r)
        # T4 -> (n - r, n - r)
        S = self.P * self.P.transpose()
        T = self.Q.transpose() * self.Q

        S2 = S[:r, r:]
        S4 = S[r:, r:]
        T3 = T[r:, :r]
        T4 = T[r:, r:]

        if hasX3:
            Xu = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            Xu = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            Xu = BlockMatrix(2, 1, [X0, X2])
        else:
            Xu = BlockMatrix(1, 1, [X0])

        Xu = Xu.subs(X0, eye(r))
        if hasX3 or hasX1:
            Xu = Xu.subs(X1, -S2 * S4 ** -1)
        if hasX3 or hasX2:
            Xu = Xu.subs(X2, -T4 ** -1 * T3)
        if hasX3:
            Xu = Xu.subs(X3, T4 ** -1 * T3 * S2 * S4 ** -1)
        pprint(Xu)
