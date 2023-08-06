import tktkrs #tktkrs ==0.1.2
from tkinter import Label
import tkinter as tk


class GifFrame(Label):
    def __init__(self,*argv,gif_path:str,**kwords):
        super().__init__(*argv,**kwords)

        self.gifinfo:list = tktkrs.gif_info(gif_path)
        self.frame_index =-1
        self.frame_all = len(self.gifinfo)
        if self.frame_all==0:
            raise Exception("gif decode fail")
        # print(self.frame_all)
        self.frames = [tk.PhotoImage(file=gif_path, format='gif -index %i' %(i)) for i in range(self.frame_all)]
        self.run()
    def run(self):
        self.frame_index=(self.frame_index+1)%self.frame_all
        self["image"] =  self.frames[self.frame_index]#self.iter.__sizeof__()
        self.after(self.gifinfo[self.frame_index],self.run)

if __name__=="__main__":
    win = tk.Tk()
    xe = GifFrame(win,gif_path=r"C:\exp1.gif")
    xe.grid(column=0,row=0,sticky="WNSE")
    win.columnconfigure(0,weight=1)
    win.rowconfigure(0,weight=1)
    win.mainloop()