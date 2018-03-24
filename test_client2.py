import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 10000

s.connect((host, port))
print(s.recv(1024).decode(encoding='utf-8'))
s.close()
