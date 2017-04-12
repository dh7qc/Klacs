import json
import socket

def Main():
	print
	host = '192.168.2.13'
	port = 5000
	s = socket.socket()
	s.connect((host, port))
	data = {}
	data['User'] = 'Brenden'		
	
	while True:
		message = input('Enter a message: ')
		data['Message'] = message
		s.send(str.encode(str(data)))
	
	s.close()
    
if __name__ == '__main__':
	Main()