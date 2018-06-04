import random
import sys


max_matr_file_length = int(sys.argv[1])
matrix_size = int(sys.argv[2])

matr_file_count = int(matrix_size / max_matr_file_length)

for i in range(matr_file_count):
    with open(f'matrix\matr{i+1}.txt', 'w', encoding='utf-8') as fm:
        for j in range(matrix_size):
                        if j >= max_matr_file_length:
                            break
                        for k in range(matrix_size):
                            fm.write(str(random.randrange(0, 999)))
                            fm.write(' ')
                        fm.write('\n')
    with open('vector\Vector.txt', 'w', encoding='utf-8') as vf:
        for k in range(matrix_size):
            vf.write(str(random.randrange(0, 999)))
            vf.write(' ')
