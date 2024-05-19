import tkinter
from tkinter import *
from tkinter import messagebox
import SocketService

import MyAuth
from entity.User import *


myAuth = MyAuth.MyAuth()
token = None


class MainGui(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        user_result = myAuth.get_user_info("ndx123")
        print(token)
        myAuth.get_user_info_with_token(token)
        admin = myAuth.admin_login()
        print(admin)
        self.user = User(user_result["result"]["name"], user_result["result"]["remark"], udp_cli.get_ip())
        self.master = master
        self.master.resizable(0, 0)
        self.pack()
        self.menu_bar = tkinter.Menu(self.master)
        self.menu_file = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="个人", menu=self.menu_file)
        self.menu_file.add_command(label="信息", command=self.user_gui)
        self.create_widgets()

    def create_widgets(self):
        self.master.config(menu=self.menu_bar)

    def user_gui(self):
        UserGui(self.user, self.master)


class Register:
    def __init__(self, master):
        self.master = master
        top = self.top = tkinter.Toplevel(master)
        top.title("[信笺]用户注册")
        top.geometry("200x300+900+400")
        top.transient(root)
        top.protocol("WM_DELETE_WINDOW", self.on_close)
        user = StringVar()
        password = StringVar()
        name = StringVar()
        remark = StringVar()
        self.user_entry = Entry(top, textvariable=user, width=15)
        self.user_label = Label(top, text="账号：")
        self.password_label = Label(top, text="密码：")
        self.password_entry = Entry(top, textvariable=password, show="*", width=15)
        self.name_label = Label(top, text="昵称：")
        self.name_entry = Entry(top, textvariable=name, width=15)
        self.remark_label = Label(top, text="备注：")
        self.remark_entry = Entry(top, textvariable=remark, width=15)
        self.register_button = Button(top, text="注册", command=self.register, width=10)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.user_entry.place(relx=0.25, rely=0.1)
        self.user_label.place(relx=0.05, rely=0.1)
        self.password_entry.place(relx=0.25, rely=0.25)
        self.password_label.place(relx=0.05, rely=0.25)
        self.name_entry.place(relx=0.25, rely=0.4)
        self.name_label.place(relx=0.05, rely=0.4)
        self.remark_entry.place(relx=0.25, rely=0.55)
        self.remark_label.place(relx=0.05, rely=0.55)
        self.register_button.place(relx=0.3, rely=0.7)

    def register(self):
        result = myAuth.register(self.user_entry.get(), self.password_entry.get(),
                                 self.name_entry.get(), self.remark_entry.get())
        code = result["code"]
        msg = result["msg"]
        messagebox.showinfo(code, msg)
        if code == 200:
            self.on_close()

    def on_close(self):
        self.master.login_button.config(state="normal")
        self.master.register_button.config(state="normal")
        self.master.user_entry.config(state="normal")
        self.master.password_entry.config(state="normal")
        self.top.destroy()


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        user = StringVar()
        passwd = StringVar()
        self.user_entry = Entry(self, textvariable=user)
        self.user_label = Label(self, text="账号：")
        self.password_label = Label(self, text="密码：")
        self.password_entry = Entry(self, textvariable=passwd, show="*")
        self.login_button = Button(self, text="登录", command=self.login, width=10)
        self.register_button = Button(self, text="注册", command=self.register, width=10)
        self.master = master
        self["width"] = 300
        self["height"] = 200
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """创建组件"""
        self.user_label.place(relx=0.1, rely=0.2)
        self.user_entry.place(relx=0.3, rely=0.2)
        self.password_label.place(relx=0.1, rely=0.4)
        self.password_entry.place(relx=0.3, rely=0.4)
        self.login_button.place(relx=0.15, rely=0.6)
        self.register_button.place(relx=0.6, rely=0.6)

    def login(self):
        global token
        user = self.user_entry.get()
        password = self.password_entry.get()
        result = myAuth.login(user, password)
        code = result["code"]
        msg = result["msg"]
        if code == 200:
            """
            销毁登录界面，新建一个父窗口为用户界面
            """
            token = result["result"]["token"]
            heart = myAuth.heartbeat(token)
            print(heart["msg"])
            self.master.destroy()
            main_gui = Tk()
            main_gui.title("XinJian")
            main_gui.geometry("300x500+1400+150")
            MainGui(main_gui)
            main_gui.mainloop()
        else:
            messagebox.showinfo(code, msg)

    def register(self, **kwargs):
        Register(self)
        self.register_button.config(state="disabled")
        self.login_button.config(state="disabled")
        self.user_entry.config(state="disabled")
        self.password_entry.config(state="disabled")


if __name__ == '__main__':
    udp_cli = SocketService.SocketLoad()
    root = Tk()
    root.title("[信笺]登录界面")
    root.geometry("300x200+700+400")
    Application(master=root)
    root.mainloop()
