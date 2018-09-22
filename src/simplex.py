import sys
from tableaux import Tableaux
import numpy as np



def read_file():
    with open('../tests/sample.txt') as f:
        content = f.readlines()
        
    tableaux = Tableaux(content)
    
    return tableaux

def main():
    print 'Starting'
    tableaux = read_file()
    print tableaux.matrix

if __name__ == "__main__":
    main()