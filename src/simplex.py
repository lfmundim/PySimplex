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
            if matrix[0][j] == 1 and matrix[i][j] == -1:
                matrix[i][j] = float(1)
    # lp._print()
    # Zera colunas canonicas
    lines = []
    for i in range(0, lp.columns):
        if matrix[0][i] == 1:
            for j in range(0, lp.lines):
                if matrix[j][i] == 1:
                    lines.append(j)

    for i in range(1, lp.lines):
        for j in range(0, lp.columns):
            if i in lines:
                matrix[0][j] = matrix[0][j]-matrix[i][j]

    lp.matrix = matrix
    print('inicio')
    lp._print()
    print('fim')   
    out = simplex(lp, True)  
    print('saida aux1')
    out._print()  
    return lp


def simplex(lp, aux):
    matrix = lp.matrix
    # lp._print()
    c_line = matrix[0]
    # Pivoteia
    if(aux):
        print('aux')
        lp._print()
    while has_negative(c_line):
        # lp._print()
        column = get_negative_column(c_line)
        # Verifica se é ilimitada
        if(not_unlimited(lp, column)):
            lp = pivoting(lp, column)
        else:
            print ('Status: ilimitado')
            print ('Certificado:')
            # printar certificado
            return
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

        print ('Status: otimo')
        print ('Objetivo: ', lp.matrix[0][-1])
        print ('Solucao: ')
        print (solution_string)
        print ('Certificado:')
        #printar certificado
    return lp

def not_unlimited(lp, column):
    matrix = lp.matrix
    for i in range(1, lp.lines):
        if matrix[i][column]>0:
            return True
    return False


def pivoting(lp, column):
    pivot = [1 for i in range(0, lp.columns-1)]
    pivot.append(sys.maxsize)
    pivot_index = 0

    # Escolhe linha pivot
    for i in range(1, lp.lines):
        if(lp.matrix[i][column] <= 0 or pivot[column] == 0):
            continue
        if(lp.matrix[i][-1]/lp.matrix[i][column] < pivot[-1]/pivot[column]):
            pivot = lp.matrix[i]
            pivot_index = i
    
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
    return lp

def create_aux_tableaux():
    aux_tableaux = read_file()
    # C Line
    # Preenche linha com 0's 
    for i in range(0, aux_tableaux.variables):
        aux_tableaux.matrix[0][i] = 0
    # Coloca 1's nas colunas identidades
    for i in range(0, aux_tableaux.aux_tableau_negatives+1):
        aux_tableaux.matrix[0][-i-1] = 1
    aux_tableaux.matrix[0][-1] = 0

    # Multiplica linhas com resultado negativo por -1
    for i in range(1, aux_tableaux.lines):
        if aux_tableaux.matrix[i][-1] < 0:
            for j in range(0, aux_tableaux.columns):
                aux_tableaux.matrix[i][j] = aux_tableaux.matrix[i][j]*-1

    return aux_tableaux

def read_file():
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()
        
    tableaux = Tableaux(content)
    
    return tableaux    

def main():
    np.set_printoptions(precision=3)
    tableaux = read_file()
    # tableaux._print()
    need_aux = True
    # Rodar aux pra todas
    # for i in range(0, tableaux.lines):
    #     if tableaux.matrix[i][-1] < 0:
    #         need_aux = True

    if(need_aux):
        aux_tableaux = create_aux_tableaux()
        aux_response = aux_simplex(aux_tableaux)
        print('saida da aux')
        aux_response._print()
        if(aux_response.matrix[0][-1]<0):
            print ('Status: inviavel')
            print ('Certificado: ')
            # printar certificado
        else:
            simplex(tableaux, False)
    else:
        simplex(tableaux, False)
    

if __name__ == "__main__":
    main()
