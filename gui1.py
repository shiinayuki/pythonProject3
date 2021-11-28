# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/26 16:31
@Author ： Shiina
@File ：gui1.py
@IDE ：PyCharm
"""
import tkinter as tk
import  tkinter.messagebox
import  pickle
window = tk.Tk()
window.title('login')
window.geometry('310x230')
# 登陆界面
tk.Label(window, text='账户：').place(x=50,y=50)
tk.Label(window, text='密码：').place(x=50, y=90)

var_usr_name = tk.StringVar()
enter_usr_name = tk.Entry(window, textvariable=var_usr_name)
enter_usr_name.place(x=100, y=50)

var_usr_pwd = tk.StringVar()
enter_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
enter_usr_pwd.place(x=100, y=90)

#登陆
def usr_log_in():
    #输入框内容
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usr_info.pickle', 'rb') as usr_file:
            usrs_info=pickle.load(usr_file)
    except:
        with open('usr_info.pickle', 'wb') as usr_file:
            usrs_info={'admin':'admin'}
            pickle.dump(usrs_info, usr_file)

    # 判断
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='###'+usr_name)
        else:
            tk.messagebox.showerror(message='ERROR!')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='用户名不能为空！')

def usr_sign_quit():
    window.destroy()

def usr_sign_up():
    def signtowcg():
        NewName = new_name.get()
        NewPwd = new_pwd.get()
        ConfirPwd = pwd_comfirm.get()
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}
        if NewName in exist_usr_info:
            tk.messagebox.showerror(message='用户名存在！')
        elif NewName == '' and NewPwd == '':
            tk.messagebox.showerror(message='用户名和密码不能为空！')
        elif NewPwd != ConfirPwd:
            tk.messagebox.showerror(message='密码前后不一致！')
        else:
            exist_usr_info[NewName] = NewPwd
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo(message='注册成功！')
                window_sign_up.destroy()

    # 新建注册窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('400x300')
    window_sign_up.title('sign_up')

    # 注册编辑框
    new_name = tk.StringVar()
    new_pwd = tk.StringVar()
    pwd_comfirm = tk.StringVar()

    tk.Label(window_sign_up, text='账户名：').place(x=90,y=50)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=160, y=50)

    tk.Label(window_sign_up, text='密码：').place(x=90,y=100)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=160, y=100)

    tk.Label(window_sign_up, text='确认密码：').place(x=90, y=150)
    tk.Entry(window_sign_up, textvariable=pwd_comfirm, show='*').place(x=160, y=150)
#确认注册
    bt_confirm = tk.Button(window_sign_up, text='确定', command=signtowcg).place(x=180,y=220)

#登录 注册按钮
bt_login = tk.Button(window,text='登录',command=usr_log_in)
bt_login.place(x=150,y=150)

window.mainloop()