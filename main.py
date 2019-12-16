
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


if __name__ == '__main__':
    main()
