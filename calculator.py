"""Module for calculating pseudoinverses"""

from sympy import *


class Calculator:
    @staticmethod
    def load_matrix(m, n):
        """
        Returns the matrix which user gives as input or None if the input is incorrect.
        """
        matrix = []
        for i in range(m):
            matrix.append(input().split())
            if len(matrix[i]) != n:
                return None
        return matrix

    # Greedy
    @staticmethod
    def find_row(A, i, j):
        m, n = A.shape
        for row in range(i + 1, m):
            if A[row, j] != 0:
                return row
        return None

    # Greedy
    @staticmethod
    def find_column(A, i, j):
        m, n = A.shape
        for column in range(j + 1, n):
            if A[i, column] != 0:
                return column
        return None

    def gauss_jordan_row(self, A):
        m, n = A.shape
        P = eye(m)

        i, j = 0, 0
        while i < m and j < n:
            # 1. step: If A[i, j] == 0 swap the ith row with some other row below to guarantee that A[i, j] != 0.
            # If all entries in the column are zero, increase j by 1.
            if A[i, j] == 0:
                row_to_swap_with = self.find_row(A, i, j)
                if row_to_swap_with is None:
                    j += 1
                    continue
                A = A.elementary_row_op(op='n<->m', row1=i, row2=row_to_swap_with)
                P = P.elementary_row_op(op='n<->m', row1=i, row2=row_to_swap_with)

            if A[i, j] != 0:
                # 2. step: Divide the ith row by A[i, j] to make the pivot entry = 1.
                k = Rational(1, A[i, j])
                if k != 1:
                    A = A.elementary_row_op(op='n->kn', row=i, k=k)
                    P = P.elementary_row_op(op='n->kn', row=i, k=k)

                # 3. step: Eliminate all other entries in the jth column by subtracting suitable multiples of the
                # ith row from the other rows.
                for row in range(m):
                    if row != i and A[row, j] != 0:
                        k = -A[row, j]
                        A = A.elementary_row_op(op='n->n+km', row=row, k=k, row2=i)
                        P = P.elementary_row_op(op='n->n+km', row=row, k=k, row2=i)

            # 4. step: Increase i by 1 and j by 1 to choose the new pivot element. Return to step 1.
            i += 1
            j += 1
        return A, P

    def gauss_jordan_column(self, A):
        m, n = A.shape
        Q = eye(n)

        i, j = 0, 0
        while i < m and j < n:
            # 1. step: If A[i, j] == 0 swap the jth column with some other column to the right to guarantee that A[i, j] != 0.
            # If all entries in the row are zero, increase i by 1.
            if A[i, j] == 0:
                column_to_swap_with = self.find_column(A, i, j)
                if column_to_swap_with is None:
                    i += 1
                    continue
                A = A.elementary_col_op(op='n<->m', col1=j, col2=column_to_swap_with)
                Q = Q.elementary_col_op(op='n<->m', col1=j, col2=column_to_swap_with)

            if A[i, j] != 0:
                # 2. step: Divide the jth column by A[i, j] to make the pivot entry = 1.
                k = Rational(1, A[i, j])
                if k != 1:
                    A = A.elementary_col_op(op='n->kn', col=j, k=k)
                    Q = Q.elementary_col_op(op='n->kn', col=j, k=k)

                # 3. step: Eliminate all other entries in the ith row by subtracting suitable multiples of the
                # jth column from the other columns.
                for column in range(n):
                    if column != j and A[i, column] != 0:
                        k = -A[i, column]
                        A = A.elementary_col_op(op='n->n+km', col=column, k=k, col2=j)
                        Q = Q.elementary_col_op(op='n->n+km', col=column, k=k, col2=j)

            # 4. step: Increase i by 1 and j by 1 to choose the new pivot element. Return to step 1.
            i += 1
            j += 1
        return A, Q

    def calculate_P_Q(self, matrix):
        if matrix is None:
            return None, None
        A = matrix.copy()

        A, P = self.gauss_jordan_row(A)
        A, Q = self.gauss_jordan_column(A)
        return P, Q

    @staticmethod
    def calculate_general_1_inverse(matrix):
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
            R = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            R = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            R = BlockMatrix(2, 1, [X0, X2])
        else:
            R = BlockMatrix(1, 1, [X0])

        R = R.subs(X0, eye(r))
        return R

    @staticmethod
    def calculate_general_12_inverse(matrix):
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
            R = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            R = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            R = BlockMatrix(2, 1, [X0, X2])
        else:
            R = BlockMatrix(1, 1, [X0])

        R = R.subs(X0, eye(r))
        if hasX3:
            R = R.subs(X3, X2 * X1)
        return R

    @staticmethod
    def calculate_general_13_inverse(matrix, P):
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
        S = P * P.transpose()

        # X1 = -S2 * S4 ** -1, it is guaranteed that S4 has inverse
        S2 = S[:r, r:]
        S4 = S[r:, r:]

        if hasX3:
            R = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            R = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            R = BlockMatrix(2, 1, [X0, X2])
        else:
            R = BlockMatrix(1, 1, [X0])

        R = R.subs(X0, eye(r))
        if hasX3 or hasX1:
            R = R.subs(X1, -S2 * S4 ** -1)
        return R

    @staticmethod
    def calculate_general_14_inverse(matrix, Q):
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
        T = Q.transpose() * Q

        # X2 = -T4 ** -1 * T3, it is guaranteed that T4 has inverse
        T3 = T[r:, :r]
        T4 = T[r:, r:]

        if hasX3:
            R = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            R = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            R = BlockMatrix(2, 1, [X0, X2])
        else:
            R = BlockMatrix(1, 1, [X0])

        R = R.subs(X0, eye(r))
        if hasX3 or hasX2:
            R = R.subs(X2, -T4 ** -1 * T3)
        return R

    @staticmethod
    def calculate_moore_penrose_inverse(matrix, P, Q):
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
        S = P * P.transpose()
        T = Q.transpose() * Q

        S2 = S[:r, r:]
        S4 = S[r:, r:]
        T3 = T[r:, :r]
        T4 = T[r:, r:]

        if hasX3:
            R = BlockMatrix(2, 2, [X0, X1, X2, X3])
        elif hasX1:
            R = BlockMatrix(1, 2, [X0, X1])
        elif hasX2:
            R = BlockMatrix(2, 1, [X0, X2])
        else:
            R = BlockMatrix(1, 1, [X0])

        R = R.subs(X0, eye(r))
        if hasX3 or hasX1:
            R = R.subs(X1, -S2 * S4 ** -1)
        if hasX3 or hasX2:
            R = R.subs(X2, -T4 ** -1 * T3)
        if hasX3:
            R = R.subs(X3, T4 ** -1 * T3 * S2 * S4 ** -1)
        return R
