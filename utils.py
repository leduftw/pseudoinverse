"""Module for handling user requests."""

# from calculator import Calculator
from operations import *

__version__ = '1.0'


class Menu:
    def __init__(self):
        # Calculator
        self.calculator = Calculator()

        # Matrices
        self.user_matrix = None
        self.general_1_inverse = None
        self.general_12_inverse = None
        self.general_13_inverse = None
        self.general_14_inverse = None
        self.moore_penrose_inverse = None

        # Flags
        self.user_matrix_loaded = False
        self.general_1_inverse_calculated = False
        self.general_12_inverse_calculated = False
        self.general_13_inverse_calculated = False
        self.general_14_inverse_calculated = False
        self.moore_penrose_inverse_calculated = False

        '''
        # Internal data structures
        keys = [c for c in char_range('a', 'z')]
        values = [Symbol(c) for c in keys]
        self.symbol_dictionary = {k: v for (k, v) in zip(keys, values)}
        '''

    def __str__(self):
        """
        Returns the options which user can choose.
        """
        return ('Izaberite jednu od sledecih opcija:\n' +
                '1. Unos matrice\n' +
                '2. Prikaz matrice\n' +
                '3. Zamenjivanje simbolickih vrednosti u matrici\n' +
                '4. Izracunavanje opsteg {1}-inverza\n' +
                '5. Izracunavanje opsteg {1, 2}-inverza\n' +
                '6. Izracunavanje opsteg {1, 3}-inverza\n' +
                '7. Izracunavanje opsteg {1, 4}-inverza\n' +
                '8. Izracunavanje Mur-Penrouzovog inverza\n' +
                '9. Kraj rada\n\n' +
                'Vas izbor: ')

    def reset_matrices(self):
        self.user_matrix = None
        self.general_1_inverse = None
        self.general_12_inverse = None
        self.general_13_inverse = None
        self.general_14_inverse = None
        self.moore_penrose_inverse = None

    def reset_flags(self):
        self.user_matrix_loaded = False
        self.general_1_inverse_calculated = False
        self.general_12_inverse_calculated = False
        self.general_13_inverse_calculated = False
        self.general_14_inverse_calculated = False
        self.moore_penrose_inverse_calculated = False

    def clear_all(self):
        self.reset_matrices()
        self.reset_flags()

    def handle_loading(self):
        self.clear_all()

        input_not_correct = True
        while input_not_correct:
            m = int(input('\nBroj vrsta u matrici: '))
            n = int(input('Broj kolona u matrici: '))
            print('\nUnesite matricu:')
            self.user_matrix = self.calculator.load_matrix(m, n)
            if self.user_matrix is None:
                print(f'Nepravilan unos matrice! Svaka vrsta mora imati tacno {n} elemenata. Pokusajte ponovo.')
            else:
                input_not_correct = False
        print()
        self.user_matrix = Matrix([self.user_matrix[row] for row in range(m)])  # changing matrix to sympy Matrix object
        self.user_matrix_loaded = True

    @staticmethod
    def print_matrix(matrix):
        print()
        pprint(matrix)
        print()

    def handle_printing(self, matrix):
        if matrix is None:
            print('Matrica ne postoji!\n')
        else:
            self.print_matrix(matrix)

    def handle_substitution(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            symbols_to_replace = input('\nUnesite oznake simbola koje zelite da zamenite: ').split()
            values_to_insert = input(
                'Unesite vrednosti kojima zelite da zamenite navedene simbole, u redosledu navodjenja: ').split()
            print()
            self.user_matrix = self.user_matrix.subs(list(zip(symbols_to_replace, values_to_insert)))

    def find_general_1_inverse(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            self.general_1_inverse = self.calculator.calculate_general_1_inverse(self.user_matrix)
            self.general_1_inverse_calculated = True
            self.handle_printing(self.general_1_inverse)

    def find_general_12_inverse(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            self.general_12_inverse = self.calculator.calculate_general_12_inverse(self.user_matrix)
            self.general_12_inverse_calculated = True
            self.handle_printing(self.general_12_inverse)

    def find_general_13_inverse(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            self.general_13_inverse = self.calculator.calculate_general_13_inverse(self.user_matrix)
            self.general_13_inverse_calculated = True
            self.handle_printing(self.general_13_inverse)

    def find_general_14_inverse(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            self.general_14_inverse = self.calculator.calculate_general_14_inverse(self.user_matrix)
            self.general_14_inverse_calculated = True
            self.handle_printing(self.general_14_inverse)

    def find_moore_penrose_inverse(self):
        if self.user_matrix is None:
            print('Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n')
        else:
            self.moore_penrose_inverse = self.calculator.calculate_moore_penrose_inverse(self.user_matrix)
            self.moore_penrose_inverse_calculated = True
            self.handle_printing(self.moore_penrose_inverse)


'''
def char_range(c1, c2):
    """
    Generates the characters from `c1` to `c2`, inclusive.
    """
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)
'''
