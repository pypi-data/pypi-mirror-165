import tkinter as tk
from tkinter import LabelFrame
from tkinter.scrolledtext import ScrolledText


class LogFrame(LabelFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Gui_Show()
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
    def Gui_Show(self):
        self.scText=ScrolledText(self)
        self.scText.grid(row=0,column=0,sticky="WNSE")
    def m_Gui_LogClear(self):
        self.scText.delete(0.0,'end')
    def m_Gui_LogInsert(self,msg,see_end:bool=False):
        self.scText.insert('end',msg+"\n")
        if see_end:
            self.scText.see('end')
