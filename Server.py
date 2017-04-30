import json
import socket
import threading
import os
import time
from Channel import Channel

# This is the Server object file that will be launched from the controller.
# This functions of this class are as follows:
#   Start the server and listen for clients trying to connect.
#   Listen to the connected clients for incoming JSON strings.
#   Send a response back to the clients with a success flag and response statement.

class Server:
    # Member Variables
    m_port = 5000
    m_host = socket.gethostbyname(socket.gethostname())
    userDatabase = {} # username, password database
    clients = []
    channels = {}
    buffer = 1024
    # Open the socket
    server_i = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # JSON template
    result = '{"username": "", "action": "result", "data": { "success_flag": "", "response": ""} }'

    # Member Functions
    def __init__(self):
        print(self.m_host)
        # Bind to the port
        try:
            self.server_i.bind((Server.m_host, Server.m_port))
        except:
            pass    # Print error to the console
        # Main loop to add new clients
        while True:
            data, addr = self.server_i.recvfrom(self.buffer)
            print(data.decode('utf-8'))
            print(addr)
            if addr not in self.clients:
                self.clients.append(addr)
                print(self.clients)
                Server.sendResult(self, conn=addr, username='', successFL=True,
                                  response='Successfully connected to server.')
            else:
                index = self.clients.index(addr)
                # Print to console print('connected to: ' +addr[0]+':'+str(addr[1]))
                t = threading.Thread(target=Server.receiving_thread, args=(self, index, data))
                t.start()

    def receiving_thread(self, i, data):
        addr = Server.clients[i]
        d1 = data.decode('utf-8')
        if d1 == 'q':
            os._exit(0)
        d2 = json.loads(d1)
        if d2['action'] == 'login' :
            # Print to console 'username' is attempting to login
            if Server.userLogin(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+ ' successfully logged in.')
                # Print to console 'username' is successfully logged in.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to log in.')
                # Print to console 'username' failed to log in.
        elif d2['action'] == 'register':
            # Print to console 'username' is attempting to register.
            if Server.userRegister(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+ ' successfully registered.')
                # Print to console 'username' has successfully registered.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to register.')
                # Print to console 'username' has failed to register.
        elif d2['action'] == 'post':
            # Print to console 'username' is attempting to post a message to a channel
            if Server.postMessage(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+ ' successfully posted to '+d2['data']['chat id']+'.')
                # Print to console 'username' has successfully posted to 'chat ID'.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to post to '+d2['data']['chat id']+'.')
                # Print to console 'username' has failed to post to 'chat ID'.
        elif d2['action'] == 'join':
            # Print to console 'username' is attempting to join 'chat ID'.
            if Server.userJoinChannel(self, data=d2, addr=addr) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+ ' successfully  joined '+d2['data']['chat id']+'.')
                # Print to console 'username' has successfully joined 'chat ID'.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to join '+d2['data']['chat id']+'.')
                # Print to console 'username' has failed to join 'chat ID'.
        elif d2['action'] == 'create chat':
            # Print to console 'username' is attempting to create 'chat ID'.
            if Server.createChannel(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+ ' successfully  created '+d2['data']['chat id']+'.')
                # Print to console 'username' has successfully created 'chat ID'.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to create '+d2['data']['chat id']+'.')
                # Print to console 'username' has failed to create 'chat ID'.
        elif d2['action'] == 'add':
            # Print to console 'username' is attempting to add 'targetUser' to 'chat ID'.
            if Server.addUser(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username']+' successfully  added ' + d2['data']['targetUser'] + ' to ' + d2['data']['chat id'] + '.')
                # Print to console 'username' has successfully added 'targetUser' to 'chat ID'.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to add ' + d2['data']['targetUser']+' to ' + d2['data']['chat id'] + '.')
                # Print to console 'username' has failed to add 'targetUser' to 'chat ID'.
        elif d2['action'] == 'ban':
            # Print to console 'username' is attempting to ban 'targetUser' from 'chat ID'.
            if Server.banUser(self, data=d2) :
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=True, response=d2['username'] + ' successfully  banned ' + d2['data']['targetUser']+' from ' + d2['data']['chat id'] + '.')
                # Print to console 'username' has successfully banned 'targetUser' from 'chat ID'.
            else:
                Server.sendResult(self, conn=addr, username=d2['username'], successFL=False, response=d2['username'] + ' failed to ban ' + d2['data']['targetUser'] + ' from ' + d2['data']['chat id'] + '.')
                # Print to console 'username' has failed to ban 'targetUser' from 'chat ID'.


    def sendResult(self, conn, username, successFL, response):
        # Print response to the console
        Server.server_i.sendto(str.encode('{"username": "'+username+'", "action": "result", "data": { "success_flag": "'+str(successFL)+'", "response": "'+response+'"} }'), conn)

    def userLogin(self, data): # should return true or false accordingly
        username = data['username']
        password = data['data']['password']
        if username in self.userDatabase:
            if self.userDatabase[username] == password:
                return True
        else:
            return False

    def userRegister(self, data): # should return true or false accordingly
        username = data['username']
        password = data['data']['password']
        if username not in self.userDatabase:
            self.userDatabase[username] = password
            print(self.userDatabase)
            return True
        else:
            return False

    def postMessage(self, data): # Should return true or false accordingly
        key = data['data']['chat id']
        user = data['username']
        if key in self.channels and user in self.channels[key].users:
            self.channels[key].postMessage(data['username'], data)
            print(self.channels[key].archive)
            return True
        else:
            return False


    def userJoinChannel(self, data, addr):  # Should return true or false accordingly
        temp = data['data']
        key = temp['chat id']
        addr = addr
        if key in self.channels:
            print(str(self.channels[key].users[data['username']]))
            self.channels[key].users[data['username']] = addr
            return True
        else:
            return False


    def createChannel(self, data): # Should return true or false accordingly
        temp = data['data']
        key = temp['chat id']
        if key not in self.channels:
            self.channels[key] = Channel(Server.server_i, data['data']['chat id'], data['username'])
            Channel.assignAdmin(self.channels[key], data['username'])
            print(self.channels)
            return True
        else:
            return False


    def addUser(self, data): # Should return true or false accordingly
        temp = data['data']
        key = temp['chat id']
        if key in self.channels:
            Channel.addUser(self.channels[key], data)
            return True
        else:
            return False

    def banUser(self, data): # Should return true or false accordingly
        temp = data['data']
        key = temp['chat id']
        if key in self.channels:
            Channel.banUser(self.channels[key], data)
            return True
        else:
            return False
