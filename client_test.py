import json
import socket
import messages


def Main():
    print("~~~~~CLIENT_TEST~~~~~")

    host = input('Enter a Host (Default = 127.0.0.1): ')
    port = int(input('Enter a Port (Default = 5000): '))
    s = socket.socket()
	
    usr = input('Enter a Username: ')
    
    s.connect((host, port))
    
    while True:
        msg = input('Enter a Message: ')
        message = messages.create_msg(usr, msg)
        s.send(str.encode(str(message)))	
    s.close()

if __name__ == '__main__':
    Main()
