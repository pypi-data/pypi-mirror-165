import tkinter as tk
from tkinter import LabelFrame

class ListFrame(LabelFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Gui_Show()
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)
        self.rowconfigure(0,weight=1)
    def Gui_Show(self):
        scbar=tk.Scrollbar(self)
        self.lb=tk.Listbox(self,selectmode="SINGLE",yscrollcommand=scbar.set)
        scbar.config(command=self.lb.yview)
        self.lb.grid(column=0,row=0,sticky="NSWE")
        scbar.grid(column=1,row=0,sticky="NS")
        self.lb.bind('<<ListboxSelect>>',self.Gui_BindDeal)
    def Gui_BindDeal(self,e):
        if self.lb.curselection()==():
            return
        print("index{}".format(self.lb.curselection()))
        print("Click{}".format(self.lb.get(self.lb.curselection())))
        self.m_CallBackFunc(self.lb.curselection()[0],self.lb.get(self.lb.curselection()))
        
    def m_ListDataToGui(self,listData:list):
        self.lb.delete(0,'end')
        for idx in listData:
            self.lb.insert('end',idx)
    def m_CallBackFunc(self,a,b):
        '''
        index|select
        '''
        print("{}-{}".format(a,b))
    def m_Update_Item(self,label_list:list):
        self.lb.delete(0,'end')
        for idx in label_list:
            self.lb.insert('end',"[{}] | {}".format(label_list.index(idx),idx))
    def m_Item_Select(self,num):
        self.lb.selection_clear(0,'end')
        self.lb.activate(num)
        self.lb.selection_set(num)
        self.lb.see(num)
