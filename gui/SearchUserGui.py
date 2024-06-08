from tkinter import messagebox
from tkinter.ttk import *
from tkinter import *
from data.DataBase import *
from entity.User import *


class SearchUserGui:
    def __init__(self, master, database: DataBase):
        self.master = master
        self.database = database
        top = self.top = Toplevel(master)
        top.title("查找用户")
        top.resizable(False, False)
        top.geometry("240x130+1000+100")
        top.wm_attributes("-toolwindow", 1)
        self.search_frame = self.SearchFrame(self, top, database)
        self.search_frame.create_widgets()
        self.search_result_frame = self.SearchResultFrame(top)
        self.search_result_frame.create_widgets()

    class SearchFrame(Frame):
        def __init__(self, sug, master, database: DataBase):
            super().__init__(master)
            self.sug = sug
            self.master = master
            self.database = database
            self["width"] = 240
            self["height"] = 35
            self["border"] = 2
            self["relief"] = "ridge"
            self.grid_propagate(False)
            self.user_var = StringVar()
            self.user_label = Label(self, text="用户名:")
            self.user_entry = Entry(self, width=15, textvariable=self.user_var)
            self.search_button = Button(self, text="查找", width=6, height=1, command=self.search_user)

        def create_widgets(self):
            self.grid(column=0, row=0, columnspan=4, pady=5)
            self.user_label.grid(column=0, row=0, padx=5)
            self.user_entry.grid(column=1, row=0, columnspan=3, padx=5)
            self.search_button.grid(column=4, row=0, padx=5)

        def search_user(self):
            user_name = self.user_var.get()
            if user_name == "":
                messagebox.showerror("提示", "请输入要查找的用户名！")
                return
            result = self.database.get_user_info(user=user_name)
            if "null" in result["name"]:
                messagebox.showerror("提示", "不存在此用户！")
                return
            self.sug.search_result_frame.create_user_widgets(User(**result))

    class SearchResultFrame(LabelFrame):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self["width"] = 240
            self["height"] = 851
            self["border"] = 2
            self["relief"] = "sunken"
            self["text"] = "查找结果"
            self.grid_propagate(False)
            self.id_var = StringVar()
            self.user_var = StringVar()
            self.motto_var = StringVar()
            self.id_label = Label(self, text="用户ID:")
            self.user_label = Label(self, text="用户名:")
            self.motto_label = Label(self, text="个性签名:")
            self.id_entry = Entry(self, textvariable=self.id_var, width=3)
            self.id_entry.config(state="disable")
            self.user_entry = Entry(self, textvariable=self.user_var, width=10)
            self.user_entry.config(state="disable")
            self.motto_entry = Entry(self, textvariable=self.motto_var, width=22)
            self.motto_entry.config(state="disable")

        def create_widgets(self):
            self.grid(column=0, row=1, rowspan=4, columnspan=4)

        def create_user_widgets(self, user: User):
            self.id_label.grid(column=0, row=2, sticky=W, padx=5)
            self.id_var.set(user.get_id())
            self.id_entry.grid(column=1, row=2, sticky=W)
            self.user_label.grid(column=2, row=2, sticky=E, padx=5)
            self.user_var.set(user.get_name())
            self.user_entry.grid(column=3, row=2, sticky=E, padx=5)
            self.motto_label.grid(column=0, row=3,sticky=W, padx=5)
            self.motto_var.set(user.get_motto())
            self.motto_entry.grid(column=1, row=3, columnspan=3, sticky=W)
