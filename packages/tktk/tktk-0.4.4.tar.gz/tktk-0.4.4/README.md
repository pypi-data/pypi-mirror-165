# tktk

#### 介绍
tkinter的增强控件，将tkinter的基础控件进行封装，给予更强大的控件功能，所有控件继承于LabelFrame进行封装，使用方法和普通控件没什么区别；

🛠
**[pypi](https://pypi.org/project/tktk/)**
**[gitee](https://gitee.com/w-8/tktk)**
#### 软件架构
软件架构说明


#### 安装教程

1.  pip install git+https://gitee.com/w-8/tktk.git
2.  pip install tktk
3.  xxxx

#### 使用说明

~~~py
import tkinter as tk
import tktk

if __name__=="__main__":
    win = tk.Tk()
    xe=tktk.LogFrame(win)
    xe.grid(column=0,row=0,sticky="WNSE")
    win.columnconfigure(0,weight=1)
    tk.Button(win,text="Insert1",command=lambda: xe.m_Gui_LogInsert("233")).grid(column=0,row=1,sticky='WNSE')
    tk.Button(win,text="Insert2",command=lambda: xe.m_Gui_LogInsert("244",True)).grid(column=0,row=2,sticky='WNSE')
    tk.Button(win,text="Clear",command=lambda: xe.m_Gui_LogClear()).grid(column=0,row=3,sticky='WNSE')
    win.mainloop()
~~~

#### 演示图片
![LogFrame](asset/ReadmeShow.gif)

#### 参与贡献

1.  Fork 本仓库
2.  拉取Fork后仓库的代码到本地
3.  提交代码
4.  新建 Pull Request





