import socket
import time

if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(('10.119.35.40', 8088))
    sk.listen(5)
    conn, addr = sk.accept()
    data = conn.recv(1024)
    print(data.decode('GBK'))
    input_data = input("请输入要发送的数据")
    conn.send(input_data.encode('GBK'))
    time.sleep(1)
    conn.close()
    sk.close()
