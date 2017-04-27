#Created by Ian Hoffmeyer and Michael Eschbacher
#client.py
#To run on campus linux machines: $ python3 client.py

import socket
import threading
import time
import messages
import signal
import sys

#Handler used to ignore KeyboardInterrupt from user.
def handler(signum, frame):
    print ('\n(ERROR!) To exit use: /exit, /quit/ or /part. (ERROR!)\n' + alias + "-> ", end='')

signal.signal(signal.SIGINT, handler)

tLock = threading.Lock()
shutdown = False

#Seperate thread to receive and print messages handed by the server.
def receving(name, sock):
    global shutdown
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(4096)
                print(data.decode('utf-8'))
                dataDic = messages.JSONdict(data.decode('utf-8'))
                if dataDic['flag'] == 0:
                    print ("\n~~~~~~~~(" + dataDic['time'] + ") " + dataDic['user'] + ": " + dataDic['message'] + '\n' + alias + "-> ", end='')
                elif dataDic['flag'] == 1 or dataDic['flag'] == 2:
                    print ("\n@@@@@@@@("  + dataDic['user'] + ") " + dataDic['message'] + '\n' + alias + "-> ", end='')
                elif dataDic['flag'] == 3:
                    print ("\n(ALERT!) "  + dataDic['message'] + " (ALERT!)"  + '\n' + alias + "-> ", end='')
                    shutdown = True
                    time.sleep(9)
                    print ("\n(ALERT!) DISCONNECTED FROM SERVER, PRESS ENTER TO EXIT (ALERT!)")
        except:
            pass

host = '0.0.0.0'
port = 0

#Handler to check successful creation of socket and successful binding of socket.
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        s.setblocking(0)
        break
    except:
        print("ERROR!) Invalid socket. (ERROR!)")
        sys.exit(0)

#Handler to check correct hostname has been entered.
while True:
    try:
        serverIP = input("Enter the hostname of the server you would like to connect to-> ")
        server = (serverIP,5000)
        s.connect(server)
        break
    except:
        print("ERROR!) Invalid hostname. (ERROR!)")

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

alias = input("Name: ")
ping = 'memes'
s.sendto(str.encode(ping), server)
time.sleep(1)
register = '{"username":"' + alias + '", "action":"register", "data": { "password":"password", "IP":"' + host + '"}}'
s.sendto(str.encode( register ) , server )
time.sleep(1)
login = '{"username":"' + alias + '", "action":"login", "data": { "password":"password", "IP":"' + host + '"}}'
s.sendto(str.encode( login ), server)
time.sleep(1)
channel_name = input("Creat Channel:  ")
create_chat = '{"username":"' + alias + '", "action":"create chat", "data": {"chat id":"'+channel_name+'", "invite only":"false", "anonymous":"false"}}'
s.sendto(str.encode( create_chat ), server)
time.sleep(1)
join = '{"username":"' + alias + '", "action":"join", "data": { "chat id":"'+channel_name+'" } }'
s.sendto(str.encode( join ), server)
time.sleep(1)
message_text = input(alias + "-> ")
post = '{"username":"' + alias + '", "action":"post", "data": { "chat id":"'+channel_name+'", "message":"'+message_text+'", "date/time":"'+ time.ctime(time.time()) +'"}}'
s.sendto(str.encode( post ), server)
time.sleep(1)

#Main loop used to send messages to the server.
while message != '/exit' and message != '/quit' and message != '/part' and shutdown != True:
    if message != '':
        send = messages.create_msg(alias,message,0)
        s.sendto(str.encode( send ) , server )
    message = input(alias + "-> ")

send = messages.create_msg(alias,"has disconnected. ", 2)
s.sendto(str.encode( send ) , server )

shutdown = True
rT.join()
s.close()

print ("\n(ALERT!) GOODBYE (ALERT!)")
