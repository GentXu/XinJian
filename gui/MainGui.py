from tkinter import ttk
from gui.SearchUserGui import *
from PIL import ImageTk, Image


class MainGui(Frame):
    def __init__(self, master, database):
        super().__init__(master)
        self.master = master
        self.database = database
        self.master.resizable(0, 0)
        # self.menu_bar = tkinter.Menu(self.master)
        # self.menu_file = tkinter.Menu(self.menu_bar, tearoff=0)
        # self.menu_bar.add_cascade(label="个人", menu=self.menu_file)
        # self.menu_file.add_command(label="信息", command=self.user_gui)
        user_img = Image.open("img/icon/user.png").resize((17, 17))
        search_img = Image.open("img/icon/search.png").resize((17, 17))
        self.tk_search_icon = ImageTk.PhotoImage(search_img)
        self.tk_user_icon = ImageTk.PhotoImage(user_img)
        self.user_button = ttk.Button(self, image=self.tk_user_icon, command=self.toggle_user_frame)
        self.search_button = ttk.Button(self, image=self.tk_search_icon, text="查 找", compound="left", width=5,
                                        command=self.search_user)
        self.create_widgets()
        self.user_frame = self.UserFrame(self)
        self.user_frame.create_widgets()
        self.my_friend_frame = self.MyFriendFrame(self)
        self.blacklist_frame = self.BlackListFrame(self)
        self.stranger_frame = self.StrangerFrame(self)

    def create_widgets(self):
        self.grid(column=0, row=0)
        self.user_button.grid(column=0, row=0, columnspan=4, sticky=W)
        self.search_button.grid(column=0, row=7, columnspan=4, sticky=E)
        # self.master.config(menu=self.menu_bar)

    def toggle_user_frame(self):
        if self.user_frame.hidden:  # 主框架为隐藏状态
            self.my_friend_frame.grid_remove()  # 隐藏好友框架
            self.blacklist_frame.grid_remove()  # 隐藏黑名单框架
            self.stranger_frame.grid_remove()  # 隐藏陌生人框架
            self.my_friend_frame.hidden = True  # 设置好友框架为隐藏状态
            self.blacklist_frame.hidden = True  # 设置黑名单框架为隐藏状态
            self.stranger_frame.hidden = True  # 设置陌生人框架为隐藏状态
            self.user_frame.grid(column=0, row=1, columnspan=4, rowspan=5)
        else:   # 主框架为显示状态
            self.user_frame.grid_remove()   # 隐藏主框架
        self.user_frame.hidden = not self.user_frame.hidden

    def search_user(self):
        SearchUserGui(self.master, self.database)

    """
    用户框架主类
    """
    class UserFrame(ttk.Frame):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.style = ttk.Style()
            self.style.configure("TFrame", background="white")
            self.style.configure("UserFrame.TFrame", background="#787b9b")
            self["relief"] = "sunken"
            self["width"] = 90
            self["height"] = 155
            self["border"] = 2
            self["style"] = "TFrame"
            self.grid_propagate(False)  # 防止Frame根据其中的控件自动调整尺寸

            self.my_friend_button = ttk.Button(self, text="我的好友", width=11, command=self.my_friend_click)
            self.stranger_button = ttk.Button(self, text="陌生人", width=11, command=self.stranger_click)
            self.blacklist_button = ttk.Button(self, text="黑名单", width=11, command=self.blacklist_click)

            self.hidden = False

        def my_friend_click(self):
            if self.master.my_friend_frame.hidden:  # 我的好友框架如果隐藏状态
                self.grid_remove()  # 删除当前框架
                self.master.my_friend_frame.create_widgets()  # 显示我的好友框架
                self.hidden = True  # 设置主框架为隐藏状态
                self.master.my_friend_frame.hidden = False  # 设置好友框架为显示状态
            else:  # 我的好友框架显示状态
                self.master.toggle_user_frame()  # 隐藏当前框架，显示主框架

        def blacklist_click(self):
            if self.master.blacklist_frame.hidden:  # 黑名单框架如果隐藏状态
                self.grid_remove()  # 删除当前框架
                self.master.blacklist_frame.create_widgets()  # 显示黑名单框架
                self.hidden = True  # 设置主框架为隐藏状态
                self.master.blacklist_frame.hidden = False  # 设置黑名单框架为显示状态
            else:  # 黑名单框架显示状态
                self.master.toggle_user_frame()

        def stranger_click(self):
            if self.master.stranger_frame.hidden:  # 陌生人框架如果隐藏状态
                self.grid_remove()  # 删除当前框架
                self.master.stranger_frame.create_widgets()  # 显示陌生人框架
                self.hidden = True  # 设置主框架为隐藏状态
                self.master.stranger_frame.hidden = False  # 设置陌生人框架为显示状态
            else:  # 陌生人框架显示状态
                self.master.toggle_user_frame()  # 隐藏当前框架，显示主框架

        def create_widgets(self):
            self.grid(column=0, row=1, columnspan=4, rowspan=6)
            self.my_friend_button.grid(column=0, row=0, columnspan=1)
            self.stranger_button.grid(column=0, row=1, columnspan=1)
            self.blacklist_button.grid(column=0, row=2, columnspan=1)

    class MyFriendFrame(UserFrame):
        def __init__(self, master):
            super().__init__(master)
            self.my_friend_frame = ttk.Frame(self, width=86, height=70, style="UserFrame.TFrame")
            self.my_friend_frame.grid_propagate(False)
            self.hidden = True

        def create_widgets(self):
            self.grid(column=0, row=1, columnspan=4, rowspan=6)
            self.my_friend_button.grid(column=0, row=0, columnspan=1)
            self.my_friend_frame.grid(column=0, row=1, rowspan=3)
            self.stranger_button.grid(column=0, row=4, columnspan=1)
            self.blacklist_button.grid(column=0, row=5, columnspan=1)

    class BlackListFrame(UserFrame):
        def __init__(self, master):
            super().__init__(master)
            self.blacklist_frame = ttk.Frame(self, width=86, height=70, style="UserFrame.TFrame")
            self.blacklist_frame.grid_propagate(False)
            self.hidden = True

        def create_widgets(self):
            self.grid(column=0, row=1, columnspan=4, rowspan=6)
            self.my_friend_button.grid(column=0, row=0, columnspan=1)
            self.stranger_button.grid(column=0, row=1, columnspan=1)
            self.blacklist_button.grid(column=0, row=2, columnspan=1)
            self.blacklist_frame.grid(column=0, row=3, rowspan=3)

    class StrangerFrame(UserFrame):
        def __init__(self, master):
            super().__init__(master)
            self.stranger_frame = ttk.Frame(self, width=86, height=70, style="UserFrame.TFrame")
            self.stranger_frame.grid_propagate(False)
            self.hidden = True

        def create_widgets(self):
            self.grid(column=0, row=1, columnspan=4, rowspan=6)
            self.my_friend_button.grid(column=0, row=0, columnspan=1)
            self.stranger_button.grid(column=0, row=1, columnspan=1)
            self.blacklist_button.grid(column=0, row=5, columnspan=1)
            self.stranger_frame.grid(column=0, row=2, rowspan=3)
