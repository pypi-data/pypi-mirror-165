import tkinter as tk
from 列表 import *
from 基本 import *
from 字符串 import *
try:
    from 游戏 import *
except (OSError, ImportError):
    pass
from 终端 import *
from 运算 import *
from 绘图 import *
from ascii码 import *
import easygui
import sys
import os
os.popen('chcp 65001')
os.popen('title rabbit控制台')
ide = tk.Tk()
ide.geometry('800x590')
ide.title('新的模块')
ide.iconbitmap('image\\rabbit.ico')
path_ = '调试'
menu = tk.Menu(ide)
fm = tk.Menu(menu,tearoff=False)
entry = tk.Text(ide,font=('华文行楷',15),width=800,height=600)
def new():
    global ide
    global entry
    global path_
    ide.title('新的模块')
    entry.delete(1.0, "end")
    path_ = '调试'
def open_():
    global path_
    global ide
    global entry
    path_ = tk.filedialog.askopenfilename()
    path_ = path_.replace("/","\\\\")
    ide.title(path_)
    entry.delete(1.0, "end")
    f = open(path_,encoding='utf-8')
    entry.insert("end",f.read())
    f.close()
def save():
    global path_
    global ide
    global entry
    if path_ == '调试' or path_ == '':
        file = easygui.enterbox(msg='请输入文件名',title='设置文件名')
        path_ = tk.filedialog.askdirectory()
        path_ = path_.replace("/","\\\\") + "\\\\" + file +'.rab'
        f = open(path_,'w',encoding='utf-8')
        f.write(entry.get('0.0','end'))
        f.close()
        ide.title(path_)
    else:
        f = open(path_,'w',encoding='utf-8')
        f.write(entry.get('0.0','end'))
        f.close()
        ide.title(path_)
def run():
    global ide
    global entry
    global path_
    print('正在运行',path_,sep='')
    try:
        exec(entry.get('0.0','end'))
    except Exception as error:
        print(error.__class__.__name__,error)
    print('程序运行结束')
fm.add_command(label='新建',command=new)
fm.add_command(label='打开',command=open_)
fm.add_command(label='保存',command=save)
menu.add_cascade(label='文件',menu=fm)
menu.add_command(label='运行',command=run)
ide.config(menu=menu)
entry.pack()
try:
    path_ = sys.argv[1]
    ide.title(path_)
    f = open(path_,encoding='utf-8')
    entry.insert("end",f.read())
    f.close()
except IndexError:
    pass
ide.mainloop()