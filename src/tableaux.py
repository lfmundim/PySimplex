import numpy as np
from fractions import Fraction
import sys


class Tableaux:
    variables = 0
    rules = 0
    lines = 0
    columns = 0
    variable_conditions = []
    matrix = []
    objective = []    
    operations_matrix = []
    original = []

    def __init__(self, content):
        print 'Reading file'
        # Pega quantidade de variaveis e restricoes
        variables = int(content[0])
        rules = int(content[1])
        print 'File read'

        print 'Getting non-neg conditions'
        # Pega condicoes de nao-negatividade
        condition_tokens = content[2].split(' ')
        variable_conditions = [int(i) for i in condition_tokens]
        print 'Success: ', variable_conditions, '\n'

        print 'Getting objective function'
        # Pega funcao objetivo * -1
        objective_tokens = content[3].split(' ')
        objective = [int(i)*-1 for i in objective_tokens]
        print 'Success: ', objective, '\n'

        # Pega matriz de operacoes auxiliar (str)
        aux_matrix = []
        for i in range (4, 4+rules):
            line_tokens = content[i].split(' ')
            aux_matrix.append(line_tokens)

        print 'Generating Identity Matrix'
        # Cria identidade para FPI
        extra = []
        for i in range(0, rules):
            aux = []
            for j in range(0, variables):
                if(i==j):
                    if(aux_matrix[i][variables] == '<='):
                        aux.append(1)
                    else:
                        aux.append(-1)
                else:
                    aux.append(0)
            extra.append(aux)
        print 'Success: ', extra, '\n'

        # Cria matriz de operacoes
        matrix = []
        for i in range(0, rules):
            aux_numbers = []
            for j in range(0, variables):
                aux_numbers.append(int(aux_matrix[i][j]))
            
            for j in range(0, variables):
                aux_numbers.append(int(extra[i][j]))
            aux_numbers.append(int(aux_matrix[i][-1]))
            matrix.append(aux_numbers)
        
        self.variable_conditions = variable_conditions
        self.variables = variables
        self.rules = rules
        self.objective = objective
        self.matrix = matrix
        self.columns = len(matrix[0])
        self.lines = len(matrix)
        self.original = matrix

        # Transforma matriz em Fraction
        for i in range(0, self.lines):
            for j in range(0, self.columns):
                self.matrix[i][j] = Fraction(self.matrix[i][j], 1)


        # Inicializa matriz de operacoes
        self.operations_matrix = np.zeros((self.variables, self.variables-1), dtype="object")
        id_index_i = 1
        id_index_j = 0
        while id_index_j < self.variables-1:
            self.operations_matrix[id_index_i][id_index_j] = 1
            id_index_i += 1
            id_index_j += 1    
        # Transforma matriz de operacoes em fractions
        for i in range(0, self.operations_matrix.shape[0]):
            for j in range(0, self.operations_matrix.shape[1]):
                self.operations_matrix[i][j] = Fraction(self.operations_matrix[i][j], 1)

    def _print(self):
        tableaux = np.concatenate((self.operations_matrix, self.matrix), axis=1)
        for i in range(0, tableaux.shape[0]):
            for j in range(0, tableaux.shape[1]):
                sys.stdout.write("%4s" % np.format_float_positional(float(tableaux[i,j]), precision=5))
                if(j != (tableaux.shape[1]-1)):
                    sys.stdout.write(', ')
            if(i != (tableaux.shape[0]-1)):
                print("\n") 
        print("\n") 
        sys.stdout.flush()
