from tkinter.messagebox import *

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

from saveAPI import *

version = 'Cubit_Yu v1.0'

ExpName = ""




success_save = lambda:showinfo(message='保存成功！！下一次不需要再次配置')
show_info = lambda:showinfo(title='帮助',message='作者：Yu0ri，一个Python学习者，一个网络安全小白\n'
                  '如果有问题，请联系作者\n'
                  '联系方式:\n'
                  'VX:Yu0ri_z\n'
                  '邮箱：jzhouyx@protonmail.com\n'
                  'Github:https://github.com/Yu0ri')

#帮助窗口代码
def menuHelp():
    show_info()


#fofa保存
def fofa_save_first():
    email = fofa_email.get()
    key = fofa_key.get()
    fofa_write(email,key)
    success_save()

#shodan保存
def shodan_save_first():
    key = shodan_key.get()
    shodan_write(key)
    success_save()


#设置窗口代码
def menuSetting():
    global fofa_email,fofa_key,shodan_key
    windows_setting = ttk.Toplevel(title='设置')
    windows_setting.iconbitmap('./image/logo.ico')
    windows_setting.geometry('1024x500+100+100')

    fofa_email = ttk.StringVar(windows_setting,value="email")
    fofa_key = ttk.StringVar(windows_setting,value="key")
    shodan_key = ttk.StringVar(windows_setting, value="key")

#fofa配置界面
    fofaLabFrame = ttk.Labelframe(windows_setting,text='fofa配置',style="INFO")
    fofaLabFrame.grid(row=0,column=0,padx=5,pady=5)
    ttk.Label(master=fofaLabFrame,text='email:').grid(row=0,column=0)
    emailEntry = ttk.Entry(master=fofaLabFrame,width=40,textvariable=fofa_email).grid(row=0,column=1,padx=3,pady=3)
    ttk.Label(master=fofaLabFrame,text='key:').grid(row=1,column=0)
    keyEntry = ttk.Entry(master=fofaLabFrame,width=40,textvariable=fofa_key).grid(row=1,column=1,padx=3,pady=3)
    textBtn_fofa = ttk.Button(master=fofaLabFrame,text='点击保存',command=fofa_save_first).grid(row=2,column=0,columnspan=2,padx=3,pady=3)

#shodan配置界面
    shodanLabFrame = ttk.Labelframe(windows_setting, text='shodan配置',style="SUCCESS")
    shodanLabFrame.grid(row=1, column=0,padx=5,pady=5)
    ttk.Label(master=shodanLabFrame,text="key:").grid(row=0,column=0)
    API_KEY = ttk.Entry(master=shodanLabFrame,width=40,textvariable=shodan_key).grid(row=0,column=1,padx=3,pady=3)
    textBtn_shodan = ttk.Button(master=shodanLabFrame, text='点击保存',style="DANGER",command=shodan_save_first).grid(row=1, column=0, columnspan=2, padx=3, pady=3)


    windows_setting.mainloop()

#Exp窗口代码
def menuExp():
    windows_Exp = ttk.Toplevel(title='Exp')
    windows_Exp.iconbitmap('./image/logo.ico')
    windows_Exp.geometry('442x350+500+300')

    list = []
    for i in ExpName.split('\n'):
        list.append(i)

    sf = ScrolledFrame(windows_Exp, autohide=True,style="INFO")
    sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for x in list:
        ttk.Button(sf,text=f"{x}").pack(fill=X,anchor=W,padx=2,pady=2)

    windows_Exp.mainloop()








