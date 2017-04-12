import os
import socket
import threading
import messages

def Main():
    print("~~~~~SERVER_TEST~~~~~")
    
    host = input('Enter a Host (Default = 127.0.0.1): ')
    port = int(input('Enter a Port (Default = 5000): '))
    s = socket.socket()
    s.bind((host,port))
    s.listen(5)
    
    print ("Server Started.")
    
    c, addr = s.accept()
    print ("Client Connected, IP : <" + str(addr) + ">" )
    
    while True:
        bits = c.recv(2048)
        bits = messages.json_str_to_dict(bits.decode('utf-8'))
        msg = bits['time'] + " - " + bits['user'] + ": " + bits['message']
        print(msg)
    s.close()

if __name__ == '__main__':
    Main()
