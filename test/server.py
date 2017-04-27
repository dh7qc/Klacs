#Created by Ian Hoffmeyer and Michael Eschbacher
#server.py
#To run on campus linux machines: $ python3 server.py

import socket
import time
import messages
import signal
import sys

#Handler to gracefully shut down upon receiving KeyboardInterrupt
def handler(signum, frame):
    global quitting
    print("\nSERVER SHUTTING DOWN IN 10 SECONDS")
    for client in clients:
        send = messages.create_msg("Server","SERVER SHUTTING DOWN IN 10 SECONDS", 3)
        s.sendto(str.encode(send), client)
    time.sleep(10)
    quitting = True
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

#Workaround for obtaining host IP using the Python Standard Library
#This list comprehension is necessary to ensure Ubuntu support (as well as Windows)
host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(so.connect(('8.8.8.8', 53)), so.getsockname()[0], so.close()) for so in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
port = 5555

clients = []

#Handler to check successful creation of socket and successful binding of socket.
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host,port))
        s.setblocking(0)
        break
    except:
        print("ERROR!) Invalid socket. (ERROR!)")
        sys.exit(0)

        
print(host)
print(port)

#Main loop used to receive and send messages from the clients.
quitting = False
print ("Server Started.")
while not quitting:
    try:
        data, addr = s.recvfrom(4096)
        
        #Allows up to 10 unique clients to communicate with the server at a time.        
        if addr not in clients and len(clients) <= 10:
            clients.append(addr)
        
        #Display messages to user
        dataDic = messages.JSONdict(data.decode('utf-8'))
        if dataDic['flag'] == 0:
            print ("\n~~~~~~~~(" + dataDic['time'] + ") " + dataDic['user'] + ": " + dataDic['message'])
        elif dataDic['flag'] == 1 or dataDic['flag'] == 2:
            print ("\n@@@@@@@@("  + dataDic['user'] + ") " + dataDic['message'])

        #Send received messages to all of the clients except for the sender.
        for client in clients:
            if client != addr:
                s.sendto(data, client)
    except:
        pass
s.close()