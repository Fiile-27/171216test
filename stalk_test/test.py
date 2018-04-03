import socket
import os
import sys
import struct
import threading

# s = socket.socket()
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# host = socket.gethostname()
# port = 10000
# s.bind((host, port))
#
# s.listen(5)
#
# conn, addr = s.accept()
# print("Client Address:", addr)
# conn.sendall("Welcome!".encode("utf-8"))
#
# size = conn.recv(1024)
# size_file = int(str(size, encoding="utf-8"))
# size_completed = 0
# conn.sendall("Transmission Started!".encode("utf-8"))
#
# file = open("tfte_new", "wb")
# count = 0
# while size_completed < size_file and count < 50:
#     file.write(conn.recv(1024))
#     print(size_completed, size_file, len(conn.recv(1024)))
#     size_completed += len(conn.recv(1024))
#     count += 1
#
# file.close()
# conn.sendall("Transmission Completed!".encode("utf-8"))
# conn.close()
# s.close()


def socket_service():
    try:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()
        port = 10000
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting for connection...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print("Accept new connection from:", addr)
    conn.sendall("Welcome!".encode("utf-8"))
    while 1:
        fileinfo_size = struct.calcsize("128sl")
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack("128sl", buf)
            filename = filename.decode("utf-8")
            fn = filename.strip('\00')
            new_filename = os.path.join("/home/fiile/Downloads/test_files/", "new_" + fn)
            print("file new name is {0}, filesize is {1}".format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print("start receiving...")

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
        conn.close()
        break

        #     data = conn.recv(1024).decode("utf-8")
        #     print("{0} client send data: {1}".format(addr, data))
        #     if data == "exit":
        #         print("Close connection: {0}".format(addr))
        #         conn.sendall("Connection closed!".encode("utf-8"))
        #         break
        #     conn.sendall(("Hello %s" % data).encode("utf-8"))
        # conn.close()


if __name__ == "__main__":
    socket_service()
