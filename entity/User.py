class User:
    def __init__(self, name, motto, ip, token):
        self.name = name
        self.motto = motto
        self.ip = ip
        self.token = token

    def get_name(self):
        return self.name

    def get_motto(self):
        return self.motto

    def get_ip(self):
        return self.ip




