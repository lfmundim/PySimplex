from __future__ import division
import sys
from tableaux import Tableaux
import numpy as np

def has_negative(line, lp):
    # for i in range (0, len(line)-1):
    for i in range (0, len(line)-1-lp.aux_tableau_negatives):
        if np.round(line[i])<0:
            # print('aqui')
            # lp._print()
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

    # Zera colunas canonicas
    lines = []
    for i in range(0, lp.columns):
        if matrix[0][i] == 1:
            for j in range(0, lp.lines):
                if matrix[j][i] == 1:
                    lines.append(j)
    # lp._print()
    for i in range(1, lp.lines):
        for j in range(0, lp.columns):
            if i in lines:
                matrix[0][j] = matrix[0][j]-matrix[i][j]

    lp.matrix = matrix
    simplex(lp, True)       
    return lp


def simplex(lp, aux):
    matrix = lp.matrix

    c_line = matrix[0]
    # Pivoteia
    while has_negative(c_line, lp):
    # for i in range(0, 2):
        # lp._print()
        column = get_negative_column(c_line)
        # Verifica se é ilimitada
        if(not_unlimited(lp, column)):
            lp = pivoting(lp, column)
        else:
            f = open("out.txt", "w+")
            f.write ('Status: ilimitado\n')
            f.write ('Certificado:\n')
            f.write ("\n")
            f.close ()
            return
    # lp._print()
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
        f = open("out.txt", "w+")
        f.write ('Status: otimo\n')
        f.write ('Objetivo: %d\n' % lp.matrix[0][-1])
        f.write ('Solucao: \n')
        f.write (solution_string)
        f.write ('\nCertificado:\n')
        f.write ("\n")
        f.close()
    return

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
        if(lp.matrix[i][column]!=0 and i != pivot_index):
            for j in range(0, lp.columns):
                # if(j==3):
                    # print('Valor ', lp.matrix[i][j])
                    # print('Linha ', i)
                    # print(lp.matrix[i][j],'=',lp.matrix[i][j],'+',abs,'*',pivot[j])
                lp.matrix[i][j] = lp.matrix[i][j]+abs*pivot[j]
        
        lp.matrix[pivot_index] = pivot
    # print('Pivoting')
    # lp._print()
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
    with open(sys.argv[1]) as f:
        content = f.readlines()
        
    tableaux = Tableaux(content)
    
    return tableaux    

def main():
    np.set_printoptions(precision=3)
    tableaux = read_file()

    need_aux = True
    # Rodar aux pra todas
    # for i in range(0, tableaux.lines):
    #     if tableaux.matrix[i][-1] < 0:
    #         need_aux = True

    if(need_aux):
        aux_tableaux = create_aux_tableaux()
        #aux_tableaux._print()
        aux_response = aux_simplex(aux_tableaux)
        # print('Fim AUX')
        if(aux_response.matrix[0][-1]<0):
            f = open("out.txt", "w+")
            f.write ('Status: inviavel\n')
            f.write ('Certificado: \n')
            f.write ("\n")
            f.close ()
            # printar certificado
        else:
            for i in range(1, aux_response.lines):
                tableaux.matrix[i] = aux_response.matrix[i]
            simplex(tableaux, False)
    else:
        simplex(tableaux, False)
    

if __name__ == "__main__":
    main()
