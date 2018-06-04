from subprocess import Popen
import socket
from threading import Thread, Lock
from itertools import count
from sys import exit


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


def callback(conn, addr, client_index):
    print(f'new listener on {addr[1]} port')
    try:
        while list_of_files:
            if conn.recv(1024) != b'ready':
                raise Exception
            with lck:
                if list_of_files:
                    data = bytes([list_of_files.pop(0)])
                else:
                    conn.close()
                    exit(0)
            print(f'[{client_index}] sending {int_from_bytes(data)}')
            conn.sendall(data)
            print(f'[{client_index}] sent {int_from_bytes(data)}, awaiting response')
            print(f'[{client_index}] recieved {conn.recv(1024)}')

    except KeyboardInterrupt:
        conn.close()


max_matr_file_length = int(input("Input max count of rows in matrix files, default = 1: ") or 2)
matrix_size = int(input("Input size of matrix and vector, default = 50: ") or 8)
workers = int(input("Input starting number of worker threads, default = 2: ") or 2)
max_workers = int(input("Input max number of worker threads, default = 10: ") or 3)

matrix_settings = [str(max_matr_file_length), str(matrix_size)]
matr_file_count = int(matrix_size / max_matr_file_length)
Popen(['python', 'file_gen.py', matrix_settings[0], matrix_settings[1]])
input()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Starting server')
sock.bind(('127.0.0.1', 56155))
sock.listen(max_workers)
list_of_files, lck = list(range(1, matrix_size+1)), Lock()

ts = []

for j in range(workers):
    Popen(['python', 'client.py'])

try:
    for j in count(1):
        conn, addr = sock.accept()
        t = Thread(target=callback,
                   args=(conn, addr, j),
                   daemon=True)
        ts.append(t)
        t.start()
except KeyboardInterrupt:
    sock.close()
