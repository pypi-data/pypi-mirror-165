import tkinter as tk

import tktkrs #rust for tktk,tktk的性能优化库
class TableFrame(tk.LabelFrame):
    def __init__(self,*args,heads=[str(idx) for idx in range(10)],weights:list=[1 for idx in range(10)],body_row=20,**Kwards):
        '''args: heads:list,weights:list[int],body_row:int;
            例:heads=["姓名","年龄","性别"],weights=[1,1,1],body_row=20;

            其中 heads设置表头信息,weights设置每列占比,body_row设置显示行数
        '''
        super().__init__(*args,**Kwards)
        self.database = tktkrs.Database()
        self.page = tk.IntVar()
        self.pages = 0
        self._inner_args=[heads,weights,body_row]
        self._design()
        self._event()
    def _design(self):
        self.table=OnlyTable(self,heads=self._inner_args[0],weights=self._inner_args[1],body_row=self._inner_args[2])
        self.table.grid(column=0,row=0,sticky='wnse')
        self.scale=tk.Scale(self,variable=self.page,from_=0,to=0,command=self._scale_update)
        self.scale.grid(column=1,row=0,sticky='ns')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
    def _event(self):
        self.scale.bind("<MouseWheel>", self._wheel)
    def _wheel(self,e):
        if e.delta<0:
            self.page.set(self.page.get()+1)
        else:
            self.page.set(self.page.get()-1)
        self._scale_update(2)
    def _scale_update(self,e):
        self.get_show_data = self.database.get_show_data(self.page.get(),self._inner_args[2])
        self.table.update_data(self.get_show_data)
    def clear_data(self):
        self.database=tktkrs.Database()
        self.pages = self.database.get_len()/self._inner_args[2]
        self.scale.configure(to=self.pages)
        self._scale_update(2)
    def insert_data(self,data,update:bool=True):
        self.database.insert_data(data)
        if update:
            self.pages = self.database.get_len()/self._inner_args[2]
            self.scale.configure(to=self.pages)
            self._scale_update(2)
    def get_all_database(self):
        return self.database.get_all()
        


class OnlyTable(tk.LabelFrame):
    def __init__(self,*args,heads=[str(idx) for idx in range(10)],weights:list=[1 for idx in range(10)],body_row=10,**Kwards):
        super().__init__(*args,**Kwards)
        self.heads = heads
        self.weights = weights
        self.body_row = body_row
        self._design()
        self._clear_items()
    def _design(self):
        [tk.Label(self,text=idx[1],relief="solid").grid(column=idx[0],row=0,sticky='wnse') for idx in enumerate(self.heads)]
        self.items = [[] for _ in range(self.body_row)]
        col = len(self.heads)
        self.items = [[tk.Label(self,text="233",width=20) for _ in range(col)] for _ in range(self.body_row)]
        [[idy[1].grid(column=idy[0],row=idx[0]+1,sticky='wnse') for idy in enumerate(idx[1])] for idx in enumerate(self.items)]
        [self.columnconfigure(idx[0],weight=idx[1]) for idx in enumerate(self.weights)]
        [self.rowconfigure(idx,weight=1) for idx in range(self.body_row+1)]
    def _clear_items(self):
        [[[idy.configure(bg="white"),idy.configure(text="")] for idy in idx] for idx in self.items]
    def update_data(self,data_list:list):
        self._clear_items()
        [[[self.items[idx[0]][idy[0]].configure(text=idy[1][0]),self.items[idx[0]][idy[0]].configure(bg=idy[1][1])] if len(idy[1])==2 else self.items[idx[0]][idy[0]].configure(text=idy[1][0]) for idy in enumerate(idx[1])] for idx in enumerate(data_list)]

if __name__=="__main__":

    win = tk.Tk()
    win.geometry("600x300")
    tk.Label().configure
    tab=TableFrame(win,text="22",heads=[str(idx) for idx in range(10)],weights=[1 for idx in range(10)],body_row=10)
    tab.grid(column=0,row=0,sticky="wnse")
    win.columnconfigure(0,weight=1)
    win.rowconfigure(0,weight=1)
    [tab.insert_data([[str(idx)*idx*idy,"red"] if idx%2 else [str(idx)] for  idy  in range(10)]) for idx  in range(11)]
    # tab.clear_data()
    win.mainloop()
