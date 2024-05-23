import threading
from tkinter import messagebox
import SocketService
from entity.User import *
from gui.UserGui import *
from data.DataBase import *


token = None
user_data = None


class MainGui(Frame):
    def __init__(self, master=None):
        super().__init__(master)
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
        UserGui(user_data, self.master)


class Register:
    def __init__(self, master):
        self.master = master
        # 窗口始终在master的上方
        top = self.top = tkinter.Toplevel(master)
        top.title("[信笺]用户注册")
        top.geometry("200x350+900+400")
        # 设为root的临时子窗口
        top.transient(root)
        # 设置windows关闭协议触发on_close方法
        top.protocol("WM_DELETE_WINDOW", self.on_close)
        # 文本框变量
        user = StringVar()
        password = StringVar()
        name = StringVar()
        motto = StringVar()
        birthday = StringVar()
        self.xb = BooleanVar()
        """
        初始化控件
        """
        self.user_entry = Entry(top, textvariable=user, width=15)
        self.user_label = Label(top, text="账号：")
        self.password_label = Label(top, text="密码：")
        self.password_entry = Entry(top, textvariable=password, show="*", width=15)
        self.name_label = Label(top, text="昵称：")
        self.name_entry = Entry(top, textvariable=name, width=15)
        self.motto_label = Label(top, text="备注：")
        self.motto_entry = Entry(top, textvariable=motto, width=15)
        self.birthday_label = Label(top, text="生日：")
        self.birthday_entry = Entry(top, textvariable=birthday, width=15)
        self.xb_label = Label(top, text="性别:")
        self.xb_radiobutton = Radiobutton(top, text="男", variable=self.xb, value=1)
        self.xb_radiobutton2 = Radiobutton(top, text="女", variable=self.xb, value=0)
        self.register_button = Button(top, text="注册", command=self.register, width=10)
        self.create_widgets()

    def create_widgets(self):
        self.user_entry.place(relx=0.25, rely=0.1)
        self.user_label.place(relx=0.05, rely=0.1)
        self.password_entry.place(relx=0.25, rely=0.25)
        self.password_label.place(relx=0.05, rely=0.25)
        self.name_entry.place(relx=0.25, rely=0.4)
        self.name_label.place(relx=0.05, rely=0.4)
        self.motto_entry.place(relx=0.25, rely=0.55)
        self.motto_label.place(relx=0.05, rely=0.55)
        self.birthday_label.place(relx=0.05, rely=0.7)
        self.birthday_entry.place(relx=0.25, rely=0.7)
        self.xb_label.place(relx=0.05, rely=0.80)
        self.xb_radiobutton.place(relx=0.25, rely=0.80)
        self.xb_radiobutton2.place(relx=0.45, rely=0.80)
        self.register_button.place(relx=0.3, rely=0.9)

    def register(self):
        result = data_base.register(user=self.user_entry.get(), name=self.name_entry.get(),
                                    passwd=self.password_entry.get(), xb=self.xb.get(),
                                    birthday=self.birthday_entry.get(), motto=self.motto_entry.get())
        if result["msg"]:
            messagebox.showinfo("提示", "注册成功！")
        else:
            messagebox.showerror("提示", "注册失败！联系管理员！")

    def on_close(self):
        self.master.login_button.config(state="normal")
        self.master.register_button.config(state="normal")
        self.master.user_entry.config(state="normal")
        self.master.password_entry.config(state="normal")
        self.top.destroy()


class Login(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self["width"] = 300
        self["height"] = 200
        self.pack()
        # 账号密码框的变量
        user = StringVar()
        self.passwd = StringVar()
        """
        初始化控件
        """
        self.user_entry = Entry(self, textvariable=user)
        self.user_label = Label(self, text="账号：")
        self.password_label = Label(self, text="密码：")
        self.password_entry = Entry(self, textvariable=self.passwd, show="*")
        self.login_button = Button(self, text="登录", command=self.login, width=10)
        self.register_button = Button(self, text="注册", command=self.register, width=10)
        self.create_widgets()

    """创建组件"""
    def create_widgets(self):
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
        result = data_base.login(user=user, passwd=password)
        if result["msg"]:
            # token = result["result"]["token"]
            # threading.Timer(200, myAuth.heartbeat, args=(token,))
            global user_data
            # 解包字典 实例化User
            user_data = User(**data_base.get_user_info(user=user))
            print(user_data.get_user())

            """
            销毁登录界面，新建一个父窗口
            """
            self.master.destroy()
            main_gui = Tk()
            main_gui.title("XinJian")
            main_gui.geometry("300x500+1400+150")
            MainGui(main_gui)
            main_gui.mainloop()
        else:
            messagebox.showerror("提示", "密码错误！请重新输入")
            self.passwd.set("")

    def register(self, **kwargs):
        Register(self)
        self.register_button.config(state="disabled")
        self.login_button.config(state="disabled")
        self.user_entry.config(state="disabled")
        self.password_entry.config(state="disabled")


if __name__ == '__main__':
    # 初始化全局协议
    udp_server = SocketService.UDPSocketLoad()
    tcp_server = SocketService.TCPSocketLoad()
    # 初始化数据库
    data_base = DataBase(tcp_server)
    # 登录界面
    root = Tk()
    root.title("[信笺]登录界面")
    root.geometry("300x200+700+400")
    Login(master=root)
    root.mainloop()
