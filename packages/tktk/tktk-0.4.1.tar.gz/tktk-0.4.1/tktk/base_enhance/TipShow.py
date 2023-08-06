import tkinter as tk
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self._wraplength=300
        self.x = self.y = 0
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,wraplength=self._wraplength, justify=tk.LEFT,
        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
        font=("微软雅黑", "12", "normal"))
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
    def setwordlenth(self,wraplen:int=300):
        self._wraplength = wraplen
 
#===========================================================
def TipShow( widget, text,wordlenth:int=300):
    '''
    arg1 控件对象
    arg2 提示信息
    '''
    toolTip = ToolTip(widget)
    toolTip.setwordlenth(wordlenth)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# if __name__=="__main__":
#     win = tk.Tk()
#     ll = tk.Label(win,text="2333")
#     ll.grid(column=0,row=0)
#     TipShow(ll,"2122233")

#     win.mainloop()
