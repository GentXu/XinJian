import socket
import threading


def recv_msg(channel, addr):
    while True:
        data = channel.recv(1024).decode("gbk")
        print(addr, ",", data)
        slist = data.split("@")
        if len(slist) != 2:
            channel.send("格式错误！".encode('gbk'))
        else:
            if slist[0] in client_map:
                target = client_map[slist[0]]
                target.send(slist[1].encode('gbk'))
            else:
                channel.send("用户没上线！".encode('gbk'))


client_map = {}
if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.119.35.40", 5418))
    server.listen(10)
    while True:
        client, client_addr = server.accept()
        key = client_addr[0] + ":" + str(client_addr[1])
        print(key, "用户连接成功")
        client_map[key] = client
        t1 = threading.Thread(target=recv_msg, args=(client, client_addr))
        t1.start()
