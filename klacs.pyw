from tkinter import *
from tkinter import ttk
from copy import deepcopy
import socket
import threading
import time
import messages
import signal
import sys
tLock = threading.Lock()

# Variables
logged_in = False
shutdown = False
current_channel = ['General']
serverIP = '10.106.57.153'
host = '0.0.0.0'
port = 0

class AppScreen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("KLACS")
        self.master.resizable(width=False, height=False)
        width = 1080
        height = 720
        self.master.minsize(width,height) #lock login screen to dimensions
        self.master.maxsize(width,height)
        widthOfScreen = master.winfo_screenwidth() # width of the screen
        heightOfScreen = master.winfo_screenheight() # height of the screen

        # calculate x and y coordinates to center screen
        x = (widthOfScreen/2) - (width/2)
        y = (heightOfScreen/2) - (height/2)
        # set the dimensions of the screen
        master.geometry('%dx%d+%d+%d' % (widthOfScreen, heightOfScreen, x, y-50))
        self.master.protocol('WM_DELETE_WINDOW', self.leave)
        self.createFrames(master)

        # Initial call of functions that are called periodically to update stuff.
        self.update_channels()
        self.update_users()
        self.request_archive()
        self.update_messages()
        return

    # Do whatever it is you need to do when the user leaves the room.
    def leave(self):
        # Close port, destroy window.
        s.close()
        self.master.destroy()
        return

    def createFrames(self, master = None):
        channelFrame = Frame(master)
        channelFrame.config(width = 225, height = 330, relief = RIDGE)
        channelFrame.place(x = 20, y = 20)
        channelLabel = Label(channelFrame, text = "Rooms:")
        channelLabel.pack()
        self.Lb = Listbox(channelFrame,selectmode="single")
        self.Lb.pack()
        self.Lb.bind('<<ListboxSelect>>', self.on_select)
        #self.Lb.insert(1, "General")

        userFrame = ttk.Frame(master)
        userFrame.config(width = 225, height = 330, relief = RIDGE)
        userFrame.place(x = 20, y = 370)
        userFrameLabel = Label(userFrame, text = "Active Users: ")
        userFrameLabel.pack()

        self.Lb2 = Listbox(userFrame,selectmode="single")
        self.Lb2.pack()

        titleFrame = ttk.Frame(master)
        titleFrame.config(width = 600, height = 20, relief = RIDGE)
        titleFrame.place(x = 265, y = 20)
        titleLabel = Label(titleFrame, text = "KLACS: ")
        titleLabel.pack()

        chatFrame = ttk.Frame(master)
        chatFrame.config(width = 600, height = 600, relief = RIDGE)
        chatFrame.place(x = 265, y = 60)

        self.chatMessages = Text(chatFrame, relief = SUNKEN, borderwidth=0, wrap=WORD, spacing1=5) # was chatMessages = Message(chatFrame, textvariable = var, width = 600)
        self.chatMessages.pack(side=LEFT,fill=Y)
        S = Scrollbar(chatFrame)
        S.pack(side=RIGHT,fill=Y)
        S.config(command=self.chatMessages.yview)
        self.chatMessages.config(yscrollcommand=S.set)
        self.chatMessages.config(state = DISABLED)


        messageFrame = ttk.Frame(master)
        messageFrame.config(width = 600, height = 20, relief = RIDGE)
        messageFrame.place(x = 265, y = 673)
        self.messageEntryVar = StringVar()
        self.messageEntry = Entry(messageFrame, textvariable = self.messageEntryVar, width = 64)
        self.messageEntry.pack(side = LEFT)

        messageSendButton = Button(messageFrame, text = "Meme It", command=self.on_send)
        messageSendButton.pack(side = RIGHT)


        serverStatusFrame = ttk.Frame(master)
        serverStatusFrame.config(width = 175, height = 500, relief = RIDGE) # was width = 175, height = 680
        serverStatusFrame.place(x = 960, y = 30) # was x = 885, y = 20
        serverSatusLabel = Label(serverStatusFrame, text = "Server Status:")
        serverSatusLabel.pack()

        backgroundLoginImage = PhotoImage(file = 'klacs-logo-transparent.gif')
        backgroundLabel = Label(self.master, image = backgroundLoginImage)
        backgroundLabel.image = backgroundLoginImage
        backgroundLabel.place(x=710, y=565)

        status = StringVar()
        serverStatus = Message(serverStatusFrame,textvariable=status, relief = SUNKEN)
        serverStatus.pack()
        status.set("Looks like the server might be up...")

    # When the button is pushed to send a message.
    def on_send(self):
        # Send the message to the server.

        msg = self.messageEntryVar.get()
        if len(msg) > 0:
            if msg[0] != '/':
                post = '{"username":"' + alias + '", "action":"post","data":{"chat id":"'+current_channel[0]+'","message":"'+ msg +'","date/time":"'+ time.ctime(time.time()) +'"}}'
                s.sendto(str.encode( post ), server)

            elif '/create' in msg: # /create
                create_channel = '{"username":"'+alias+'", "action":"create chat", "data": {"chat id":"'+msg[8:]+'", "invite only":"false", "anonymous":"false"}}'
                s.sendto(str.encode( create_channel ), server)

            elif '/join' in msg and msg[6:] != current_channel[0]:
                join_channel = '{"username":"'+alias+'", "action":"join", "data": {"chat id":"'+msg[6:]+'"}}'
                s.sendto(str.encode( join_channel ), server)
                current_channel[0] = msg[6:]
                self.chatMessages.config(state = NORMAL)
                self.chatMessages.delete(1.0, END)
                self.chatMessages.config(state = DISABLED)
                self.request_archive()

            elif '/help' in msg:
                pass

            self.messageEntry.delete(0, END)
        return

    # This function is called when a channel is selected from the channels list.
    def on_select(self,evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        # Make sure this only works if they click on a channel and not an empty space.
        if len(value) > 0 and value != current_channel[0]:
            # Send request to join channel.
            join_channel = '{"username":"'+alias+'", "action":"join", "data": {"chat id":"'+value+'"}}'
            s.sendto(str.encode( join_channel ), server)

            # Assume we are able to join the channel, update current channel value.
            current_channel[0] = value

            # Clear existing messages from text widget.
            self.chatMessages.config(state = NORMAL)
            self.chatMessages.delete(1.0, END)
            self.chatMessages.config(state = DISABLED)

            self.request_archive()
        return

    # This is what is updating the messages from the server.
    def update_messages(self):
        # Enable chat text widget so it can be modified.
        self.chatMessages.config(state = NORMAL)

        # Attempt to received data from server.
        try:
            data, addr = s.recvfrom(4096)
            #self.chatMessages.insert(END, '\n' + data.decode('utf-8')) # print(data.decode('utf-8'))
            dataDic = messages.json_str_to_dict(data.decode('utf-8'))

            if dataDic['action'] == 'post':
                self.chatMessages.insert(END, '> ' + dataDic['username'] + ': ' + dataDic['message'] + '\n')

            elif dataDic['action'] == 'request chat ids':
                lst = dataDic['data']['response'].split(', ')
                lst = lst[:len(lst)]

                self.Lb.delete(0,END)
                for i in range(len(lst)):
                    self.Lb.insert(i, lst[i])

            elif dataDic['action'] == 'request user ids':
                lst = dataDic['data']['response'].split(', ')
                lst = lst[:len(lst)]

                self.Lb2.delete(0,END)
                for i in range(len(lst)):
                    self.Lb2.insert(i, lst[i])

            elif dataDic['action'] == 'request archive':
                lst = dataDic['data']['response'].split('; ')
                for item in lst:
                    if item[0] != ' ':
                        self.chatMessages.insert(END, '> ' + item[item.find(':',18)+2:] + '\n')

        except:
            pass

        # Disable chat text widget.
        self.chatMessages.config(state = DISABLED)

        # Re-calls this function every 30ms
        self.after(30, self.update_messages)
        return

    def update_channels(self):
        # send request to server for chat ids
        request_chat = '{"username":"' + alias + '", "action":"request chat ids", "data": {"response":""}}'
        s.sendto(str.encode( request_chat ), server)

        # Updates channels list every 2 seconds
        self.after(2000, self.update_channels)

    def update_users(self):
        # send request to server for user ids
        request_users = '{"username":"' + alias + '", "action":"request user ids", "data": {"response":""}}'
        s.sendto(str.encode( request_users ), server)

        # Updates users list every 3 seconds.
        self.after(3000, self.update_users)

    def request_archive(self):
        #request archive
        req_archive = '{"username":"' + alias + '", "action":"request archive", "data": {"chat id":"'+current_channel[0]+'","response":""}}'
        s.sendto(str.encode( req_archive ), server)
        return

class Login(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("KLACS")
        self.master.resizable(width=False, height=False)
        width = 360
        height = 300
        self.master.minsize(width,height) #lock login screen to dimensions
        self.master.maxsize(width,height)
        widthOfScreen = master.winfo_screenwidth() # width of the screen
        heightOfScreen = master.winfo_screenheight() # height of the screen

        # calculate x and y coordinates to center screen
        x = (widthOfScreen/2) - (width/2)
        y = (heightOfScreen/2) - (height/2)
        # set the dimensions of the screen
        master.geometry('%dx%d+%d+%d' % (widthOfScreen, heightOfScreen, x, y))

        backgroundLoginImage = PhotoImage(file = 'klacs-logo.gif')
        backgroundLabel = Label(self.master, image = backgroundLoginImage)
        backgroundLabel.image = backgroundLoginImage
        backgroundLabel.pack()

        self.pack()
        self.createWidgets()
        return

    def createWidgets(self):
        lightBlueColor = "#aad7f4"

        self.userNameLabel = Label(self.master, text = "User Name:")
        self.userNameLabel.place(x = 40, y = 160)

        self.userNameVar = StringVar()
        self.userNameEntry = Entry(self.master, textvariable = self.userNameVar, bg = lightBlueColor)
        self.userNameEntry.place(x = 120, y = 160)

        self.passNameLabel = Label(self.master, text="Password:")
        self.passNameLabel.place(x = 40, y = 200)

        self.passNameVar = StringVar()
        self.passNameEntry = Entry(self.master, textvariable= self.passNameVar, bg = lightBlueColor, show = "*")
        self.passNameEntry.place(x = 120, y = 200)

        self.loginButton = Button(self.master, text = "Login", command=self.on_login)
        self.loginButton.pack()
        self.loginButton.place(x = 90, y = 245)

        self.registerButton = Button(self.master, text = "Register", command=self.on_register)
        self.registerButton.pack()
        self.registerButton.place( x = 180, y = 245)

    def on_register(self):
        # Register and login when register button is pressed.
        global alias
        alias = deepcopy(self.userNameVar.get())
        reg = '{"username":"' + self.userNameVar.get() + '", "action":"register", "data": { "password":"' + self.passNameVar.get() + '", "IP":"' + host + '"}}'
        s.sendto(str.encode( reg ) , server )
        # Login after registration
        log = '{"username":"' + self.userNameVar.get() + '", "action":"login", "data": { "password":"' + self.passNameVar.get() + '", "IP":"' + host + '"}}'
        s.sendto(str.encode( log ), server)

        # Disable register/signin buttons after registering... should probably check that they actually registered.
        self.loginButton.config(state = DISABLED)
        self.registerButton.config(state = DISABLED)

        # Destroy login window in order to go to chat window
        self.master.destroy()
        return

    def on_login(self):
        # Login when login button is pressed.
        global alias
        alias = deepcopy(self.userNameVar.get())
        log = '{"username":"' + self.userNameVar.get() + '", "action":"login", "data": { "password":"' + self.passNameVar.get() + '", "IP":"' + host + '"}}'
        s.sendto(str.encode( log ), server)

        # Disable register/signin buttons after logging in... should probably check that the user was actually able to login.
        self.loginButton.config(state = DISABLED)
        self.registerButton.config(state = DISABLED)
        # Destroy login window in order to go to chat window
        self.master.destroy()
        return

def run_login():
    root = Tk()
    loginScreen = Login(root)
    backgroundLoginImage = PhotoImage(file='Slack-logo-2.gif')
    loginScreen.mainloop()

def run_app():
    root = Tk()
    app = AppScreen(root)
    app.mainloop()

def receving(name, sock):
    global shutdown
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(4096)
                print(data.decode('utf-8'))
                dataDic = messages.json_str_to_dict(data.decode('utf-8'))
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

#---------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    # Handler to check successful creation of socket and successful binding of socket.
    while True:
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((host, port))
            s.setblocking(0)
            break
        except:
            print("ERROR!) Invalid socket. (ERROR!)")
            sys.exit(0)

    # Handler to check correct hostname has been entered.
    while True:
        try:
            global server
            server = (serverIP,5000)
            s.connect(server)
            break
        except:
            print("ERROR!) Invalid hostname. (ERROR!)")

    # Send random thing
    time.sleep(.1)
    ping = 'memes'
    s.sendto(str.encode('memes'), server)

    # Start thread for login.
    run_login()

    # Now logged in. Create thread for chat.
    run_chat_thread = threading.Thread(target=run_app)
    run_chat_thread.start()

    # Join default channel.

    j = '{"username":"' + alias + '", "action":"join", "data": { "chat id":"General" } }'
    s.sendto(str.encode( j ), server)
    time.sleep(.2)

    # Send message saying that I joined default channel...
    post = '{"username":"' + alias + '", "action":"post", "data": { "chat id":"General", "message":"* Entered the chatroom *", "date/time":"'+ time.ctime(time.time()) +'"}}'
    s.sendto(str.encode( post ), server)


# * Main runs here *
if __name__ == "__main__":
    main()
