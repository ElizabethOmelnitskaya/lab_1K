import socket
from os.path import join


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 56155))

try:
    while True:
        sock.sendall(b'ready')
        file_index = int_from_bytes(sock.recv(1024))
        if file_index == 0:
            break
        file_to_process = join('matrix', f'matr{file_index}.txt')
        vector = join('vector', 'Vector.txt')
        ansList = []
        ans = 0
        with open(file_to_process, 'r') as fm:
            print(f'processing file {file_to_process}')
            matr = [line.split() for line in fm]
            #print('matr = ', matr)
            with open(vector, 'r') as fv:
                vect = [line.split() for line in fv]
                #print('vect = ', vect)
                for row in matr:
                    ans = 0
                    m = [int(i) * int(j) for i, j in zip(row, vect[0])]
                    ans = sum(m)
                    ansList.append(ans)
                print(ansList)

        ans_file = join('ans', f'ans{file_index}.txt')
        with open(ans_file, 'w') as ansS:
            for an in ansList:
                ansS.write(str(an))
                ansS.write(' ')
        sock.send(b'done')
except KeyboardInterrupt:
    print('\nserver terminated')
    sock.close()
