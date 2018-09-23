from __future__ import division
import sys
from tableaux import Tableaux
import numpy as np

def has_negative(line):
    for i in range (0, len(line)-1):
        if line[i]<0:
            return True
    return False

def get_negative_column(line):
    for i in range(0, len(line)):
        if line[i]<0:
            return i

def aux_simplex(lp):
    matrix = lp.matrix

    # Positiva a identidade
    for i in range(1, lp.lines):
        for j in range(0, lp.columns):
            if matrix[0][j] == -1 and matrix[i][j] == -1:
                matrix[i][j] = 1

    # print 'AQUI DIAXO'
    # lp._print()
    # Zera colunas canonicas
    for i in range(1, lp.lines):
        for j in range(0, lp.columns):
            matrix[0][j] = matrix[0][j]-matrix[i][j]
    
    simplex(lp, True)            
    return lp


def simplex(lp, aux):
    matrix = lp.matrix
    # print 'Matrix:'
    # lp._print()

    c_line = matrix[0]
    # print c_line

    while has_negative(c_line):
    # for i in range(0,3): # Debug purposes
        column = get_negative_column(c_line)
        if(not_unlimited(lp, column)):
            pivoting(lp, column)
            # lp._print()
        else:
            print 'Status: ilimitado'
            print 'Certificado:'
            # printar certificado
            return
    # print 'pv return ', pivoting_return
    if(not aux):
        # Printa solucao do simplex otimo
        solution_string = ''
        for i in range (0, lp.variables):
            temp = 0
            line = 0
            for j in range(1, lp.lines):
                if lp.matrix[j][i] == 1 and line == 0:
                    line = j
                    temp = lp.matrix[j][-1]
                elif lp.matrix[j][i] != 0 and line != 0:
                    line = 0
                    temp = 0
            solution_string = solution_string+str(temp)+' '

        print 'Status: otimo'
        print 'Objetivo: ', lp.matrix[0][-1]
        print 'Solucao: '
        print solution_string
        print 'Certificado:'
        #printar certificado
    return

def not_unlimited(lp, column):
    matrix = lp.matrix
    for i in range(1, lp.lines):
        if matrix[i][column]>0:
            return True
    print 'Unlimited!'
    return False


def pivoting(lp, column):
    pivot = [1 for i in range(0, lp.columns-1)]
    pivot.append(sys.maxint)
    pivot_index = 0

    # Escolhe linha pivot
    for i in range(1, lp.lines):
        if(lp.matrix[i][column] <= 0 or pivot[column] == 0):
            continue
        if(lp.matrix[i][-1]/lp.matrix[i][column] < pivot[-1]/pivot[column]):
            pivot = lp.matrix[i]
            pivot_index = i

    # print 'column ',column
    # print 'pivot ',pivot
    
    # Item pivo = 1
    divisor = pivot[column]
    for i in range(0, len(pivot)):
        pivot[i] = pivot[i]/divisor

    # Pivoteamento
    for i in range(0, lp.lines):    
        abs = lp.matrix[i][column]*-1

        if(lp.matrix[i][column]==0 or i == pivot_index):
            continue
        for j in range(0, lp.columns):
            lp.matrix[i][j] = lp.matrix[i][j]+abs*pivot[j]
        
        lp.matrix[pivot_index] = pivot
    # print 'final ', lp.matrix[0][-1]

def create_aux_tableaux():
    aux_tableaux = read_file()

    # C Line
    for i in range(0, aux_tableaux.variables):
        aux_tableaux.matrix[0][i] = 0
    for i in range(aux_tableaux.variables, aux_tableaux.columns-1):
        aux_tableaux.matrix[0][i] = 1
    aux_tableaux.matrix[0][-1] = 0

    for i in range(1, aux_tableaux.lines):
        if aux_tableaux.matrix[i][-1] < 0:
            for j in range(0, aux_tableaux.columns):
                aux_tableaux.matrix[i][j] = aux_tableaux.matrix[i][j]*-1

    return aux_tableaux

def read_file():
    #with open(sys.argv[1]) as f:
    with open('../tests/3b.txt') as f:
        content = f.readlines()
        
    tableaux = Tableaux(content)
    
    return tableaux

#def generate_new_tableaux(lp):
    

def main():
    #print 'Starting'
    np.set_printoptions(precision=3)
    tableaux = read_file()

    need_aux = False
    for i in range(0, tableaux.lines):
        if tableaux.matrix[i][-1] < 0:
            need_aux = True

    if(need_aux):
        aux_tableaux = create_aux_tableaux()
        aux_response = aux_simplex(aux_tableaux)
        
        if(aux_response.matrix[0][-1]<0):
            print 'Status: inviavel'
            print 'Certificado: '
            # printar certificado
        else:
            #generate_new_tableaux(aux_response)
            simplex(tableaux, False)
    else:
        simplex(tableaux, False)
    

if __name__ == "__main__":
    main()
