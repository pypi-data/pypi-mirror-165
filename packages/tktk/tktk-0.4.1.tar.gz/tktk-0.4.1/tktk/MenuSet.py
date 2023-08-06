from tkinter import Menu
import tkinter as tk
class MenuSet(Menu):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Gui_Show()
    def Gui_Show(self):
        self.add_command(label="导入",command=lambda :self.KeyDeal("Import"))
        self.add_command(label="导出",command=lambda :self.KeyDeal("Export"))
        self.add_command(label="保存",command=lambda :self.KeyDeal("Save"))
    def KeyDeal(self,action:str):
        if action=="Import":
            self.m_CallBackImport()
        elif action=="Export":
            self.m_CallBackExport()
        elif action=="Save":
            self.m_CallBackSave()
    def m_CallBackImport(self):
        print("Import")
    def m_CallBackExport(self):
        print("Export")
    def m_CallBackSave(self):
        print("Save")

