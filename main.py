
from sympy import *
from menu import Menu

__version__ = '1.0'


def main():
    init_printing(use_unicode=True, use_latex='mathjax')
    menu = Menu()

    while True:
        print(menu)
        command = int(input())

        if command == 1:  # matrix loading
            menu.handle_loading()
        elif command == 2:  # matrix printing
            menu.handle_printing(menu.user_matrix)
        elif command == 3:  # symbols substitution
            menu.handle_substitution()
        elif command == 4:  # general {1}-inverse
            menu.find_general_1_inverse()
        elif command == 5:  # general {1, 2}-inverse
            menu.find_general_12_inverse()
        elif command == 6:  # general {1, 3}-inverse
            menu.find_general_13_inverse()
        elif command == 7:  # general {1, 4}-inverse
            menu.find_general_14_inverse()
        elif command == 8:  # moore-penrose inverse
            menu.find_moore_penrose_inverse()
        elif command == 9:  # quit
            break
        else:  # unknown command
            print('Nepoznata komanda. Pokusajte ponovo.\n')


def main1():
    """
    keys = [c for c in char_range('a', 'z')]
    values = [Symbol(c) for c in keys]
    symbol_dict = {k: v for (k, v) in zip(keys, values)}
    # print(symbol_dict)
    A, m, n = load_matrix()

    A = Matrix([A[row] for row in range(m)])
    pprint(A)
    B, m, n = load_matrix()
    B = Matrix([B[row] for row in range(m)])
    pprint(B)
    C = A + B
    pprint(C)
    pprint(C.subs('a', 23))
    """
    menu = Menu()
    menu.handle_loading()
    A = menu.user_matrix
    m, n = A.shape
    temp = A.row_join(eye(m))
    pprint(A)
    pprint(temp)
    """
    print(m, n)
    A = A.col_insert(n, eye(m))
    pprint(A)
    A = A.rref(pivots=False)
    pprint(A)
    P = A[: m, n: m + n]
    pprint(P)
    A = A[: m, : n]
    A = A.row_insert(m, zeros(1, n))
    pprint(A)
    """
    """
    A = A.T
    A = A.col_insert(m, eye(n))
    pprint(A)
    A = A.rref(pivots=False)
    pprint(A)
    A = A.T
    Q = A[m: m + n, : n]
    pprint(Q)
    """


def main2():
    menu = Menu()
    menu.handle_loading()
    A = menu.user_matrix
    pprint(A.pinv())


if __name__ == '__main__':
    main()
