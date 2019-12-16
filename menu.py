"""Module for handling user requests."""

from sympy import *
from calculator import Calculator


class Menu:
    def __init__(self):
        # Calculator
        self.calculator = Calculator()

        # Matrices
        self.user_matrix = None
        self.P = None
        self.Q = None
        self.R = None
        self.general_1_inverse = None
        self.general_12_inverse = None
        self.general_13_inverse = None
        self.general_14_inverse = None
        self.moore_penrose_inverse = None

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
        self.P = None
        self.Q = None
        self.R = None
        self.general_1_inverse = None
        self.general_12_inverse = None
        self.general_13_inverse = None
        self.general_14_inverse = None
        self.moore_penrose_inverse = None

    def handle_loading(self):
        self.reset_matrices()

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
        self.user_matrix = Matrix(
            [self.user_matrix[row] for row in range(m)])  # converting matrix to sympy Matrix object

    @staticmethod
    def print_matrix(matrix, message=''):
        print(message)
        pprint(matrix)
        print()

    def handle_printing(self, matrix, message='', err='Matrica ne postoji!\n'):
        if matrix is None:
            print(err)
        else:
            self.print_matrix(matrix, message)

    @staticmethod
    def user_matrix_not_loaded_message(message='Matrica nije uneta! Prvo unesite matricu, a zatim pokusajte ponovo.\n'):
        print(message)

    def handle_substitution(self):
        if self.user_matrix is None:
            self.user_matrix_not_loaded_message()
        else:
            symbols_to_replace = input('\nUnesite oznake simbola koje zelite da zamenite: ').split()
            values_to_insert = input(
                'Unesite vrednosti kojima zelite da zamenite navedene simbole, u redosledu navodjenja: ').split()
            print()
            self.user_matrix = self.user_matrix.subs(list(zip(symbols_to_replace, values_to_insert)))

    def handle_inverse(self, general_1_inverse=False, general_12_inverse=False, general_13_inverse=False, general_14_inverse=False, moore_penrose_inverse=False):
        if self.user_matrix is None:
            self.user_matrix_not_loaded_message()
        else:
            # First find P and Q
            if self.P is None or self.Q is None:
                self.P, self.Q = self.calculator.calculate_P_Q(self.user_matrix)

            # And then find particular inverse
            if general_1_inverse:
                self.R = self.calculator.calculate_general_1_inverse(self.user_matrix)
                self.general_1_inverse = block_collapse(self.Q * self.R * self.P)
            elif general_12_inverse:
                self.R = self.calculator.calculate_general_12_inverse(self.user_matrix)
                self.general_12_inverse = block_collapse(self.Q * self.R * self.P)
            elif general_13_inverse:
                self.R = self.calculator.calculate_general_13_inverse(self.user_matrix, self.P)
                self.general_13_inverse = block_collapse(self.Q * self.R * self.P)
            elif general_14_inverse:
                self.R = self.calculator.calculate_general_14_inverse(self.user_matrix, self.Q)
                self.general_14_inverse = block_collapse(self.Q * self.R * self.P)
            elif moore_penrose_inverse:
                self.R = self.calculator.calculate_moore_penrose_inverse(self.user_matrix, self.P, self.Q)
                self.moore_penrose_inverse = block_collapse(self.Q * self.R * self.P)
            else:
                print('Bad arguments passed.')  # this should never happen if used properly
                return

            # Print Q, R and P
            self.handle_printing(self.Q, 'Q = ')
            self.handle_printing(self.R, 'R = ')
            self.handle_printing(self.P, 'P = ')

            # Print requested inverse (Q * R * P)
            # self.handle_printing(self.Q * self.R * self.P, 'X = Q * R * P = ')
            msg = 'X = Q * R * P = '
            if general_1_inverse:
                self.handle_printing(self.general_1_inverse, message=msg)
            elif general_12_inverse:
                self.handle_printing(self.general_12_inverse, message=msg)
            elif general_13_inverse:
                self.handle_printing(self.general_13_inverse, message=msg)
            elif general_14_inverse:
                self.handle_printing(self.general_14_inverse, message=msg)
            elif moore_penrose_inverse:
                self.handle_printing(self.moore_penrose_inverse, message=msg)
                self.handle_printing(self.user_matrix.pinv().applyfunc(simplify), message="= ")

    def find_general_1_inverse(self):
        self.handle_inverse(general_1_inverse=True)

    def find_general_12_inverse(self):
        self.handle_inverse(general_12_inverse=True)

    def find_general_13_inverse(self):
        self.handle_inverse(general_13_inverse=True)

    def find_general_14_inverse(self):
        self.handle_inverse(general_14_inverse=True)

    def find_moore_penrose_inverse(self):
        self.handle_inverse(moore_penrose_inverse=True)
