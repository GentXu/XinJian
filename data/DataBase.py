import json


class DataBase:
    def __init__(self, tcp_service):
        self.tcp_service = tcp_service

    def register(self, **kwargs):
        kwargs["interface"] = "soft/register"
        data = json.dumps(kwargs)
        try:
            self.tcp_service.send_msg(data)
            return self.tcp_service.recv_msg()
        except Exception as ex:
            print(ex)

    def login(self, **kwargs):
        kwargs["interface"] = "soft/login"
        data = json.dumps(kwargs)
        try:
            self.tcp_service.send_msg(data)
            return self.tcp_service.recv_msg()
        except Exception as ex:
            print(ex)

    def get_user_info(self, **kwargs):
        kwargs["interface"] = "soft/get_user_info"
        data = json.dumps(kwargs)
        try:
            self.tcp_service.send_msg(data)
            return self.tcp_service.recv_msg()
        except Exception as ex:
            print(ex)
