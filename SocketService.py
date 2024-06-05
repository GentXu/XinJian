import json
import socket
import threading


class UDPSocketLoad:
    def __init__(self):
        self.host = '10.134.86.51'
        self.port = 25555
        self.udp_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = None
        self.initialize()
        # 开一个线程接受服务端消息
        threading.Thread(target=self.recv_msg).start()

    def get_ip(self):
        return self.ip

    """
    向服务端发送消息
    """
    def send_msg(self, msg):
        self.udp_cli.sendto(msg.encode('gbk'), (self.host, self.port))

    """
    处理服务端的消息
    """
    def recv_msg(self):
        while True:
            data, addr = self.udp_cli.recvfrom(1024)
            mod_msg = data.decode('gbk')
            split = mod_msg.split('@')
            if "Server" in split[0]:
                self.server_msg(split[0], split[1])
            if split[0] == 'Client':
                return split[1]

    def server_msg(self, code, msg):
        if "1" in code:
            self.ip = msg
            print(self.ip)

    def initialize(self):
        self.send_msg("Client@initialize")


class TCPSocketLoad:
    def __init__(self):
        try:
            self.host = '10.134.86.51'
            self.port = 25555
            self.tcp_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_cli.connect((self.host, self.port))
        except ConnectionRefusedError as ex:
            print(ex)
            exit()

    """
    服务端消息处理
    """
    def recv_msg(self):
        data = self.tcp_cli.recv(1024).decode('utf-8')
        dict_data = json.loads(data)
        return dict_data

    """
    向服务端发送消息
    """
    def send_msg(self, msg):
        self.tcp_cli.sendall(msg.encode('utf-8'))


if __name__ == '__main__':
    tcp = TCPSocketLoad()
