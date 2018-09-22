from __future__ import division
import sys
from tableaux import Tableaux
import numpy as np

def has_negative(line):
    for i in line:
        if i<0:
            return True
    return False

def get_negative_column(line):
    for i in range(0, len(line)):
        if line[i]<0:
            return i

def simplex(lp):
    matrix = lp.matrix
    print 'Matrix:'
    lp._print()

    c_line = matrix[0]
    print c_line

    while has_negative(c_line):
    # for i in range(0,3): # Debug purposes
        column = get_negative_column(c_line)
        if(not_unlimited(lp, column)):
            pivoting(lp, column)
            lp._print()
        else:
            break

def not_unlimited(lp, column):
    matrix = lp.matrix
    for i in range(1, lp.lines):
        if matrix[i][column]>0:
            return True
    print 'Unlimited!'
    return False


def pivoting(lp, column):
    pivot = [1 for i in range(0, lp.columns-1)]
    pivot.append(1000000)
    c_line = lp.matrix[0]

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
    

def read_file():
    with open('../tests/sample.txt') as f:
        content = f.readlines()
        
    tableaux = Tableaux(content)
    
    return tableaux

def main():
    print 'Starting'
    np.set_printoptions(precision=3)
    tableaux = read_file()
    simplex(tableaux)
    

if __name__ == "__main__":
    main()
