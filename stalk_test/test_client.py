import socket
import os
import sys
import struct

# s = socket.socket()
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# host = socket.gethostname()
# port = 10000
#
# s.connect((host, port))
# # print(s.recv(1024).decode("utf-8"))
#
# ret_bytes = s.recv(1024)
# print(str(ret_bytes, encoding="utf-8"))
#
# size = os.stat("tfte").st_size
# s.sendall(str(size).encode("utf-8"))
#
# s.recv(1024)
#
# file = open("tfte", "rb")
# for b in file:
#     s.sendall(b)
# s.close()


def socket_client():
    try:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()
        port = 10000
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024).decode("utf-8"))
    while 1:
        # data = input("Input:")
        # s.sendall(data.encode("utf-8"))
        # print(s.recv(1024).decode("utf-8"))
        # if data == "exit":
        #     break

        filepath = "./tfte"
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath).encode("utf-8"), os.stat(filepath).st_size)
            s.send(fhead)
            print("client filepath: %s" % filepath)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print("%s file send over..." % filepath)
                    break
                s.send(data)
        s.close()
        break
    # s.close()


if __name__ == "__main__":
    socket_client()
