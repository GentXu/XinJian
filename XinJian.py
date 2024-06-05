from tkinter import messagebox
import SocketService
from entity.User import *
from gui.MainGui import *
from gui.UserGui import *
from data.DataBase import *
from PIL import ImageTk, Image
from utils.AESUtil import *

token = None
user_data = None


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
        # 账号密码框的变量
        self.user = StringVar()
        self.passwd = StringVar()
        self.is_remember = BooleanVar()
        self.is_remember.set(True)
        self.is_stealth = BooleanVar()
        """
        初始化控件
        """
        pil_image = Image.open("img/logo.jpeg").resize((45, 45))
        self.img = ImageTk.PhotoImage(pil_image)

        self.logo = ttk.Label(self, image=self.img)
        self.split = ttk.Frame(self, borderwidth=1, relief="groove", width=300, height=2)
        self.user_entry = ttk.Combobox(self, textvariable=self.user, width=17)
        self.user_entry.bind("<<ComboboxSelected>>", self.load_user_password_cache)
        self.user_label = ttk.Label(self, text="用户账号：")
        self.password_label = ttk.Label(self, text="用户口令：")
        self.password_entry = ttk.Entry(self, textvariable=self.passwd, show="*", width=20)
        self.remember_passwd = ttk.Checkbutton(self, text="记住密码", variable=self.is_remember,
                                               onvalue=True, offvalue=False)
        self.stealth = ttk.Checkbutton(self, text="隐身登录", variable=self.is_stealth, onvalue=True, offvalue=False)
        self.login_button = ttk.Button(self, text="登录", command=self.login, width=10)
        self.register_button = ttk.Button(self, text="注册", command=self.register, width=10)

        self.columnconfigure(2, weight=1)

        self.create_widgets()

    """创建组件"""
    def create_widgets(self):
        self.load_user_cache()
        self.grid(column=0, row=0)
        self.logo.grid(column=0, row=0, rowspan=2, sticky=W)
        self.user_label.grid(column=1, row=0, rowspan=2, sticky=SW)
        self.user_entry.grid(column=2, row=0, rowspan=2, columnspan=6, sticky=SW)
        self.password_label.grid(column=1, row=2, sticky=SW, pady=10)
        self.password_entry.grid(column=2, row=2, columnspan=6, sticky=W)
        self.remember_passwd.grid(column=1, row=4, columnspan=1)
        self.stealth.grid(column=2, row=4, columnspan=1)
        self.split.grid(column=0, row=5, columnspan=7, pady=7)
        self.login_button.grid(column=1, row=6)
        self.register_button.grid(column=2, row=6, columnspan=1)
        # self.user_label.place(relx=0.1, rely=0.2)
        # self.user_entry.place(relx=0.3, rely=0.2)
        # self.password_label.place(relx=0.1, rely=0.4)
        # self.password_entry.place(relx=0.3, rely=0.4)
        # self.login_button.place(relx=0.15, rely=0.6)
        # self.register_button.place(relx=0.6, rely=0.6)

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
            # 如果勾选了记住密码就将密码存到本地
            if self.is_remember.get():
                self.save_password()
            else:
                self.un_save_password()
            """
            销毁登录界面，新建一个父窗口
            """
            self.master.destroy()
            main_gui = Tk()
            main_gui.title("")
            main_gui.geometry("90x230+1400+150")
            main_gui.attributes("-toolwindow", 2)
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

    """
    保存密码 保存前检查一下有没有重复的用户
    """
    def save_password(self):
        with open("cache/account.txt", 'r+') as file:
            account_dict = {
                "user": self.user_entry.get(),
                "password": self.password_entry.get()
            }
            aes = encrypt(json.dumps(account_dict), "xinjiankehuduan1")
            for line in file.readlines():
                de_line = decrypt(line, "xinjiankehuduan1")
                de_dict = json.loads(de_line)
                if de_dict["user"] == self.user_entry.get():
                    return
            file.write(aes + "\n")
            file.close()

    def un_save_password(self):
        with open("cache/account.txt", 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                de_line = decrypt(line, "xinjiankehuduan1")
                de_dict = json.loads(de_line)
                if de_dict["user"] == self.user_entry.get():
                    lines[index] = ""
            file.close()
        with open("cache/account.txt", 'w') as file:
            file.writelines(lines)
            file.close()

    def load_user_cache(self):
        with open("cache/account.txt", 'r') as file:
            for line in file.readlines():
                de_line = decrypt(line, "xinjiankehuduan1")
                de_dict = json.loads(de_line)
                values = list(self.user_entry['values'])
                values.append(de_dict["user"])
                values1 = tuple(values)
                self.user_entry['values'] = values1

    def load_user_password_cache(self, event):
        user = self.user_entry.get()
        with open("cache/account.txt", 'r') as file:
            for line in file.readlines():
                de_line = decrypt(line, "xinjiankehuduan1")
                de_dict = json.loads(de_line)
                if de_dict["user"] == user:
                    self.passwd.set(de_dict["password"])


if __name__ == '__main__':
    # 初始化全局协议
    # udp_server = SocketService.UDPSocketLoad()
    tcp_server = SocketService.TCPSocketLoad()
    # 初始化数据库
    data_base = DataBase(tcp_server)
    # 登录界面
    root = Tk()
    root.title("XinJian用户登录")
    root.resizable(False, False)
    root.geometry("300x170+700+400")
    Login(root)
    root.mainloop()
