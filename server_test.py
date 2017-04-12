import socket
import threading
import os

def Main():
    host = '192.168.2.13'
    port = 5000
    s = socket.socket()
    s.bind((host,port))
    s.listen(5)
    print ("Server Started.")
    c, addr = s.accept()
    print ("client connedted ip:<" + str(addr) + ">" )
    while True:
        x = c.recv(2048)
        print(x)
    s.close()

if __name__ == '__main__':
    Main()
