import tkinter as tk

import time
class StatusFrame(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.strvar = tk.StringVar()
        self.MesList=["","","",""]
        self.columnconfigure(0,weight=1)
        self.statusbar = tk.Label(self,relief="sunken",anchor="sw",textvariable=self.strvar)
        
        self.statusbar.grid(column=0,row=0,sticky="WE")
        self.RunThread()
    def ShowMessage(self):
        while True:
            self.m_UpdateTime()
            self.strvar.set(" || ".join(self.MesList))
            time.sleep(1)
    @staticmethod
    def GetTimeStr():
        '''
        返回日期字符串 如211103_161722
        '''
        return time.strftime(" %y年%m月%d日 %H:%M:%S", time.localtime())
   
    def RunThread(self):
        self.after(500,self.RunThread)
        self.m_UpdateStatus(0)
        self.m_UpdatePercent(0)
        self.ShowMessage()

    def m_UpdateInfo(self,msg):
        self.MesList[3]="Info:{}".format(msg)
    def m_UpdateStatus(self,index):
        '''
        0.Ready 1.Running 2.Finish 3.Fail 
        '''
        self.MesList[2]=["Ready","Running","Finish","Fail"][index]
        self.statusbar["bg"]=["green","yellow","green","red"][index]
        if index == 0 or index == 2:
            self.m_UpdatePercent([0,100][index>0])
    def m_UpdatePercent(self,pros):
        self.MesList[1]="{}>{} {:>3d}%".format("="*int(pros/10),"="*(10-int(pros/10)),pros)
    def m_UpdateTime(self):
        self.MesList[0]=self.GetTimeStr()

