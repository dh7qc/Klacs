from tkinter import *
from klacsGUI import *



def run_login():
    root = Tk()
    loginScreen = Login(root)
    backgroundLoginImage = PhotoImage(file='Slack-logo-2.gif')
    loginScreen.mainloop()

def run_app():
    root = Tk()
    app = AppScreen(root)
    app.mainloop()

run_login()