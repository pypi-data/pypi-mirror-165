from tkinter import Button
import tkinter as tk

from PIL import ImageSequence,Image


class RollingLabel(Button):
    def __init__(self,*argv,gif_path:str,**kwords):

        super().__init__(*argv,**kwords)
        im = Image.open(gif_path)
        imm = tk.PhotoImage(gif_path)
        print(list(gif_path))
        print(imm)
        # self.iter = list(ImageSequence.Iterator(im))
        self.frames = [tk.PhotoImage(file=gif_path, format='gif -index %i' %(i)) for i in range(26)]
        self.run()
    def run(self):
        self.frames.append(self.frames.pop(0))
        self["image"] =  self.frames[0]#self.iter.__sizeof__()
        self.after(100,self.run)

if __name__=="__main__":
    win = tk.Tk()
    xe = RollingLabel(win,gif_path=r"D:\coded\filestore\ww.gif")
    xe.grid(column=0,row=0,sticky="WNSE")
    win.columnconfigure(0,weight=1)
    win.rowconfigure(0,weight=1)
    win.mainloop()