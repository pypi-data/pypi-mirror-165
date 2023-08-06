from tkinter import Label
import tkinter as tk
class RollingLabel(Label):
    def __init__(self,*argv,textvar:tk.StringVar="",fps=500,**kwords):

        super().__init__(*argv,**kwords)
        self._roing_run = True
        self._label_var = textvar
        self._fps = fps
        if textvar !="":
            self["text"]=self._label_var.get()+" <"
            self._label_var.trace("w",self.callback)
        self.roing()
    def callback(self,*args):
        self["text"]=self._label_var.get()+" <"
    def roing(self):
        word = self["text"]
        if len(word)>1 and self._roing_run:
            self["text"]=word[1:]+word[0]
        self.after(self._fps,self.roing)
    def update_fps(self,fps:int):
        self._fps = fps
    def roing_pause(self,switch=True):
        self._roing_run=switch

    

if __name__=="__main__":
    pass
    # win = tk.Tk()
    # x = tk.StringVar()
    # x.set("1234567890")
    # RollingLabel(textvar=x,fps=100).pack()

    # x.set("111222333")
    # win.mainloop()