from tkinter import *

class AppScreen(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("KLACS")
        self.master.resizable(width=False, height=False)
        self.master.minsize(1080,720)
        self.master.maxsize(1080,720)
        self.pack()
        self.createWidgets()
        return

    def createWidgets(self):
        memeButton = Button(self.master, text = "CLICK HERE FOR MEMES", command = self.master.quit)
        memeButton.pack({"side":"top"})
        return


class Login(Frame):


    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.title("KLACS")
        self.master.minsize(320,240)
        #self.master.maxsize(320,240)

        backgroundLoginImage = PhotoImage(file = 'Slack-logo-2.gif')
        backgroundLabel = Label(self.master, image = backgroundLoginImage)
        backgroundLabel.image = backgroundLoginImage
        backgroundLabel.pack()



        self.pack()
        self.createWidgets()

        return

    def createWidgets(self):

        lightBlueColor = "#aad7f4"

        userNameLabel = Label(self.master, text = "User Name")
        userNameLabel.pack()

        userNameVar = StringVar()
        userNameEntry = Entry(self.master, textvariable = userNameVar, bg = lightBlueColor)
        userNameEntry.pack(pady = 2)

        passNameLabel = Label(self.master, text="Password")
        passNameLabel.pack(pady = 2)

        passNameVar = StringVar()
        passNameEntry = Entry(self.master, textvariable=passNameVar, bg = lightBlueColor)
        passNameEntry.pack(pady=2)

        loginButton = Button(self.master, text = "Login for Dank Memes")
        loginButton.pack()


        return