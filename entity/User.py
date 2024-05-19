import tkinter
from tkinter import *
import XinJian


class User:
    def __init__(self, name, remark, ip):
        self.name = name
        self.remark = remark
        self.ip = ip

    def get_name(self):
        return self.name

    def get_remark(self):
        return self.remark

    def get_ip(self):
        return self.ip


class UserGui:
    def __init__(self,user, master=None):
        self.master = master
        top = self.top = tkinter.Toplevel(master)
        top.title("个人信息")
        top.wm_attributes("-toolwindow", 1)
        top.resizable(False, False)
        top.transient(self.master)
        top.geometry("200x200+1200+200")
        self.user_label = Label(top, text="昵称：")
        self.user_name = Label(top, text=user.get_name())
        self.remark_label = Label(top, text="备注：")
        self.remark = Label(top, text=user.get_remark())
        self.ip_label = Label(top, text="本机IP:")
        self.ip = Label(top, text=user.get_ip())
        self.create_widgets()

    def create_widgets(self):
        self.user_label.place(relx=0.03, rely=0.1)
        self.user_name.place(relx=0.25, rely=0.1)
        self.remark_label.place(relx=0.03, rely=0.3)
        self.remark.place(relx=0.25, rely=0.3)
        self.ip_label.place(relx=0.03, rely=0.5)
        self.ip.place(relx=0.25, rely=0.5)


