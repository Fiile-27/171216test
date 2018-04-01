from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class PrpCrypt:  # 定义一个类
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, filename):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        fp = open(filename, "r")
        fp_encrypt = open(filename + "_new", "w")
        content = fp.read()
        count = len(content)
        add = length - (count % length)
        content = content + ("\0" * add)
        fp_encrypt.write(b2a_hex(cryptor.encrypt(content)).decode("utf-8"))
        fp.close()
        fp_encrypt.close()
        return filename + "_new"

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, filename):
        cryptor = AES.new(self.key, self.mode, self.key)
        fp = open(filename, "r")
        content = fp.read()
        plain_text = cryptor.decrypt(a2b_hex(content))
        return plain_text.strip().decode("utf-8").strip("\x00")


pc = PrpCrypt('abcdefghijklmnop')  # 自己设定的密钥
e = pc.encrypt("tfte")
d = pc.decrypt(e)
print(e, d)
