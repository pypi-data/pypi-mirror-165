from doctest import master
import tkinter
from tkinter import *
import os
import time

class pypopup:
    def newpopup(popupheight=False, popupwidth=False):
        master = Tk()
        canvas = Canvas(height=popupheight, width=popupwidth)
        canvas.pack()
        master.mainloop()
    def newframe(popuprelx=False, popuprely=False, popuprelheight=False, popuprelwidth=False, bgcolor=False):
        global master
        frame = Frame(master, bg=bgcolor)
        frame.place(relx=popuprelx, rely=popuprely, relheight=popuprelheight, relwidth=popuprelwidth)

pypopup.newpopup(popupheight=450, popupwidth=750)
