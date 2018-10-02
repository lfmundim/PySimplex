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
    aux_tableau_negatives = 0

    def __init__(self, content):
        # Pega quantidade de variaveis e restricoes
        variables = int(content[0])
        rules = int(content[1])

        # Pega condicoes de nao-negatividade
        condition_tokens = content[2].split(' ')
        variable_conditions = [int(i) for i in condition_tokens]

        # Pega funcao objetivo * -1
        objective_tokens = content[3].split(' ')
        objective = [float(i)*-1 for i in objective_tokens]

        # Pega matriz de operacoes auxiliar (str)
        aux_matrix = []
        for i in range (4, 4+rules):
            line_tokens = content[i].split(' ')
            aux_matrix.append(line_tokens)

        # Cria identidade para FPI
        extra = []
        geq_rows = []
        for i in range(0, rules):
            aux = []
            for j in range(0, rules):
                if(i==j):
                    if(aux_matrix[i][variables] == '>='):
                        aux.append(-1)
                    else:
                        aux.append(1)
                    geq_rows.append(i)
                else:
                    aux.append(0)
            extra.append(aux)


        if(len(geq_rows)>0):
            self.aux_tableau_negatives = len(geq_rows)
            for i in range(0, len(geq_rows)):
                aux = []
                for j in range(0, rules):
                    if(geq_rows[i]==j):
                        aux.append(1)
                    else:
                        aux.append(0)    
                extra.append(aux)
        else:
            self.aux_tableau_negatives = variables
        
        # Cria matriz de operacoes
        matrix = []
        c_vector = []
        for i in objective:
            c_vector.append(i)
        for i in range(0, len(extra)+1):
            c_vector.append(0)
        matrix.append(c_vector)            

        for i in range(0, rules):
            aux_numbers = []
            for j in range(0, variables):
                aux_numbers.append(float(aux_matrix[i][j]))
            
            for j in range(0, len(extra)):
                aux_numbers.append(float(extra[j][i]))
            aux_numbers.append(float(aux_matrix[i][-1]))
            matrix.append(aux_numbers)

        self.variable_conditions = variable_conditions
        self.variables = variables
        self.rules = rules
        self.objective = objective
        self.matrix = matrix
        self.columns = len(matrix[0])
        self.lines = len(matrix)
        self.original = matrix
        self.operations_matrix = matrix

    def _print(self):
        np.set_printoptions(precision=3)
        tableaux = self.matrix
        print('\n'.join([''.join(['{:7}'.format(round(item, 2)) for item in row]) for row in tableaux]))
        print ('\n')
