import tkinter
from tkinter import *


class UserGui:
    def __init__(self, user, master=None):
        self.master = master
        self.user = user
        top = self.top = tkinter.Toplevel(master)
        top.title("个人信息")
        top.wm_attributes("-toolwindow", 1)
        top.resizable(False, False)
        top.transient(self.master)
        top.geometry("200x200+1200+200")
        self.id_label = Label(top, text="ID：")
        self.id = Label(top, text=self.user.get_id())
        self.user_label = Label(top, text="昵称：")
        self.user_name = Label(top, text=self.user.get_name())
        self.motto_label = Label(top, text="个性签名：")
        self.motto = Label(top, text=self.user.get_motto())
        self.ip_label = Label(top, text="本机IP:")
        self.ip = Label(top, text=self.user.get_ip())
        self.change_button = Button(top, text="修改资料", command=self.change_user)
        self.create_widgets()

    def create_widgets(self):
        self.id_label.place(relx=0.03, rely=0.0)
        self.id.place(relx=0.35, rely=0.0)
        self.user_label.place(relx=0.03, rely=0.1)
        self.user_name.place(relx=0.35, rely=0.1)
        self.motto_label.place(relx=0.03, rely=0.3)
        self.motto.place(relx=0.35, rely=0.3)
        self.ip_label.place(relx=0.03, rely=0.5)
        self.ip.place(relx=0.35, rely=0.5)
        self.change_button.place(relx=0.1, rely=0.7)

    def change_user(self):
        ChangeUserInfoGui(self.user, self, self.master)
        self.change_button.config(state="disabled")


class ChangeUserInfoGui:
    def __init__(self, user, father, master=None):
        self.master = master
        self.father = father
        top = self.top = tkinter.Toplevel(master)
        top.title("修改个人信息")
        top.wm_attributes("-toolwindow", 1)
        top.protocol("WM_DELETE_WINDOW", self.on_close)
        top.resizable(False, False)
        top.transient(master)
        top.geometry("200x300+1300+300")

    def on_close(self):
        self.father.change_button.config(state="normal")
        self.top.destroy()