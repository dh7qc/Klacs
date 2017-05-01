from tkinter import *
from tkinter import ttk
import socket
import threading
import time
import messages
import signal
from copy import deepcopy
import sys
tLock = threading.Lock()

# Variables
logged_in = False
shutdown = False
serverIP = '192.168.1.57'
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
        self.update_messages()
        
        return
    
    # Do whatever it is you need to do when the user leaves the room. 
    def leave(self):
        # * send message saying user is leaving ? or send quit command to server?* 
        
        # Close port, destroy window.
        s.close()
        self.master.destroy()

    def createFrames(self, master = None):
        channelFrame = Frame(master)
        channelFrame.config(width = 225, height = 330, relief = RIDGE)
        channelFrame.place(x = 20, y = 20)
        channelLabel = Label(channelFrame, text = "Rooms:")
        channelLabel.pack()
        Lb = Listbox(channelFrame,selectmode="single")
        Lb.pack()
        Lb.insert(1, "default")
        Lb.insert(2, "this_channel_doesnt_exist")

        userFrame = ttk.Frame(master)
        userFrame.config(width = 225, height = 330, relief = RIDGE)
        userFrame.place(x = 20, y = 370)
        userFrameLabel = Label(userFrame, text = "Active Users: ")
        userFrameLabel.pack()
        
        Lb2 = Listbox(userFrame,selectmode="single")
        Lb2.pack()
        Lb2.insert(1, "person1")
        Lb2.insert(2, "otherperson")

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
        
        #self.chatMessages.insert(END, "hello \n \n \n \n b  heyyyy")
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
        serverStatusFrame.config(width = 175, height = 680, relief = RIDGE) # was width = 175, height = 680
        serverStatusFrame.place(x = 960, y = 30) # was x = 885, y = 20
        serverSatusLabel = Label(serverStatusFrame, text = "Server Status:")
        serverSatusLabel.pack()
        
        status = StringVar()
        serverStatus = Message(serverStatusFrame,textvariable=status, relief = SUNKEN)
        serverStatus.pack()
        status.set("Looks like the server might be up...")

    # When the button is pushed to send a message.
    def on_send(self):
        # Send the message to the server.
        msg = self.messageEntryVar.get()
        if len(msg) > 0:
            post = '{"username":"' + alias + '", "action":"post", "data": { "chat id":"'+channel_name+'", "message":"'+ msg +'", "date/time":"'+ time.ctime(time.time()) +'"}}'
            s.sendto(str.encode( post ), server)
            self.messageEntry.delete(0, END)
            # Update the gui. 
            self.chatMessages.config(state = NORMAL)
            self.chatMessages.insert(END, '\n> ' + alias + ': ' + msg)
            self.chatMessages.config(state = DISABLED)
        return
    
    # This is what is updating the messages from the server. 
    def update_messages(self):
        self.chatMessages.config(state = NORMAL)
        try:
            data, addr = s.recvfrom(4096)
            #self.chatMessages.insert(END, '\n' + data.decode('utf-8')) # print(data.decode('utf-8'))
            dataDic = messages.json_str_to_dict(data.decode('utf-8'))
            self.chatMessages.insert(END, '\n> ' + dataDic['username'] + ': ' + dataDic['data']['message'])
            ''''
            if dataDic['flag'] == 0:
                #self.chatMessages.insert(END,("\n~~~~~~~~(" + dataDic['time'] + ") " + dataDic['user'] + ": " + dataDic['message'] + '\n' + alias + "-> "))
                pass
            elif dataDic['flag'] == 1 or dataDic['flag'] == 2:
                #self.chatMessages.insert(END,("\n@@@@@@@@("  + dataDic['user'] + ") " + dataDic['message'] + '\n' + alias + "-> "))
                pass
            elif dataDic['flag'] == 3:
                #self.chatMessages.insert(END, ("\n(ALERT!) "  + dataDic['message'] + " (ALERT!)"  + '\n' + alias + "-> "))
                time.sleep(.5)
                print ("\n(ALERT!) DISCONNECTED FROM SERVER, PRESS ENTER TO EXIT (ALERT!)")
                '''
        except:
            pass
            
        self.chatMessages.config(state = DISABLED)

        self.after(50, self.update_messages) # Re-calls this function every 50ms
        
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
    global channel_name
    channel_name = 'General'
    j = '{"username":"' + alias + '", "action":"join", "data": { "chat id":"' + channel_name + '" } }'
    s.sendto(str.encode( j ), server)
    time.sleep(.2)
    
    # Send message saying that I joined default channel...
    post = '{"username":"' + alias + '", "action":"post", "data": { "chat id":"'+channel_name+'", "message":"* Entered the chatroom *", "date/time":"'+ time.ctime(time.time()) +'"}}'
    s.sendto(str.encode( post ), server)
    

# * Main runs here *             
if __name__ == "__main__":
    main()