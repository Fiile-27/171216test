import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 10000
s.bind((host, port))

s.listen(1)

while 1:
    conn, addr = s.accept()
    print("Client Address:", addr)
    msg = "Welcome!"
    conn.send(msg.encode(encoding='utf-8'))
    conn.close()
