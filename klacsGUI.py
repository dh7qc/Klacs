from tkinter import *
from tkinter import ttk

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

        self.createFrames(master)

        return

    def createFrames(self, master = None):

        channelFrame = Frame(master)
        channelFrame.config(width = 225, height = 330, relief = RIDGE)
        channelFrame.place(x = 20, y = 20)
        channelLabel = Label(channelFrame, text = "Rooms:")
        channelLabel.pack()


        userFrame = ttk.Frame(master)
        userFrame.config(width = 225, height = 330, relief = RIDGE)
        userFrame.place(x = 20, y = 370)
        userFrameLabel = Label(userFrame, text = "Active Users: ")
        userFrameLabel.pack()

        titleFrame = ttk.Frame(master)
        titleFrame.config(width = 600, height = 20, relief = RIDGE)
        titleFrame.place(x = 265, y = 20)
        titleLabel = Label(titleFrame, text = "KLACS: ")
        titleLabel.pack()

        chatFrame = ttk.Frame(master)
        chatFrame.config(width = 600, height = 600, relief = RIDGE)
        chatFrame.place(x = 265, y = 60)
        chatMessages = Message(chatFrame, width = 600)
        chatMessages.pack()

        messageFrame = ttk.Frame(master)
        messageFrame.config(width = 600, height = 20, relief = RIDGE)
        messageFrame.place(x = 265, y = 673)
        messageEntryVar = StringVar()
        messageEntry = Entry(messageFrame, textvariable = messageEntryVar, width = 64)
        messageEntry.pack(side = LEFT)

        messageSendButton = Button(messageFrame, text = "Meme It")
        messageSendButton.pack(side = RIGHT)


        serverStatusFrame = ttk.Frame(master)
        serverStatusFrame.config(width = 175, height = 680, relief = RIDGE)
        serverStatusFrame.place(x = 885, y = 20)
        serverSatusLabel = Label(serverStatusFrame, text = "Server Status:")
        serverSatusLabel.pack()


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

        userNameLabel = Label(self.master, text = "User Name:")
        userNameLabel.place(x = 40, y = 160)

        userNameVar = StringVar()
        userNameEntry = Entry(self.master, textvariable = userNameVar, bg = lightBlueColor)
        userNameEntry.place(x = 120, y = 160)

        passNameLabel = Label(self.master, text="Password:")
        passNameLabel.place(x = 40, y = 200)

        passNameVar = StringVar()
        passNameEntry = Entry(self.master, textvariable=passNameVar, bg = lightBlueColor, show = "*")
        passNameEntry.place(x = 120, y = 200)

        loginButton = Button(self.master, text = "Login")
        loginButton.place(x = 90, y = 245)

        registerButton = Button(self.master, text = "Register")
        registerButton.place( x = 180, y = 245)
        return
