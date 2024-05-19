import socket
import threading


class SocketLoad:
    def __init__(self):
        self.host = '222.187.254.111'
        self.port = 15061
        self.udp_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = None
        self.initialize()
        threading.Thread(target=self.recv_msg).start()

    def get_ip(self):
        return self.ip

    def send_msg(self, msg):
        self.udp_cli.sendto(msg.encode('gbk'), (self.host, self.port))

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
