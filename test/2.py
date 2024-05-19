import socket

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('10.119.35.40', 8088))
    client.send('你好'.encode('GBK'))
    data = client.recv(1024)
    print(data.decode('GBK'))
