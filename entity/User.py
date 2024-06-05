class User:
    def __init__(self, id, name, motto, ip, user, birthday, xb):
        self.name = name
        self.motto = motto
        self.ip = ip
        self.user = user
        self.birthday = birthday
        self.xb = xb
        self.id = id

    def get_name(self):
        return self.name

    def get_motto(self):
        return self.motto

    def get_ip(self):
        return self.ip

    def get_user(self):
        return self.user

    def get_birthday(self):
        return self.birthday

    def get_id(self):
        return self.id

    def get_xb(self):
        if self.xb == 1:
            return "男"
        else:
            return "女"



