from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


def encrypt(msg, aes_key):
    try:
        if len(aes_key) != 16:
            return ""
        raw = aes_key.encode('utf-8')
        cipher = AES.new(raw, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(msg.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as ex:
        return "数据加密时发生异常"


def decrypt(e_msg, aes_key):
    try:
        if len(aes_key) != 16:
            return ""
        raw = aes_key.encode('utf-8')
        cipher = AES.new(raw, AES.MODE_ECB)
        encrypted = base64.b64decode(e_msg)
        original = unpad(cipher.decrypt(encrypted), AES.block_size)
        return original.decode('utf-8')
    except Exception as ex:
        return "数据加密时发生异常"


if __name__ == '__main__':
    message = "123123"
    key = "xinjiankehuduan1"
    en_msg = encrypt(message, key)
    de_msg = decrypt(en_msg, key)
    print(f'E: {en_msg}')
    print(f'D: {de_msg}')
