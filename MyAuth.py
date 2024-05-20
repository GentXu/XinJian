import hashlib
import json
import platform
import time
import requests
import wmi


class MyAuth:
    """构造器，一些基础信息"""
    def __init__(self):
        self.skey = "55a419f8-af3a-4765-9bd8-baf9bcbc9a58"
        self.vkey = "B8E2DCF7-0ADA-4C54-AABD-742D0852890B"
        self.genkey = "ndxshishuaibi666"
        self.device_info = platform.platform()
        self.device_code = self.get_machine_code()
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
    """获得sign"""
    def get_sign(self, data):
        sign = ""
        sorted_data = dict(sorted(data.items()))
        for key in sorted_data:
            value = sorted_data[key]
            sign = sign + str(key) + "=" + str(value) + "&"
        hash_object = hashlib.md5()
        hash_object.update((sign + "gen_key=" + self.genkey).encode('utf-8'))
        sign = hash_object.hexdigest()
        return sign

    """用户注册"""
    def register(self, account, passwd, name, motto):
        reg_url = "http://47.103.131.3:7943/myauth/soft/register"
        data = {
            "device_info": self.device_info,
            "device_code": self.device_code,
            "user": account,
            "pass": passwd,
            "name": name,
            "qq": motto,
            "timestamp": str(time.time())[:10]
        }
        payload = json.dumps({
            "data": data,
            "skey": self.skey,
            "vkey": self.vkey,
            "sign": self.get_sign(data)
        })
        response = requests.request("POST", reg_url, headers=self.headers, data=payload)
        return response.json()

    """用户登录"""
    def login(self, account, passwd):
        login_url = "http://47.103.131.3:7943/myauth/soft/login"
        data = {
            "device_info": self.device_info,
            "device_code": self.device_code,
            "user": account,
            "pass": passwd,
            "timestamp": str(time.time())[:10]
        }
        payload = json.dumps({
            "data": data,
            "skey": self.skey,
            "vkey": self.vkey,
            "sign": self.get_sign(data)
        })
        response = requests.request("POST", login_url, headers=self.headers, data=payload)
        return response.json()

    """查询用户基本信息"""
    def get_user_info(self, user):
        url = "http://47.103.131.3:7943/myauth/web/queryUserInfo?user=" + user + "&skey=" + self.skey
        payload = {}
        response = requests.request("GET", url, headers=self.headers, data=payload)
        return response.json()

    """修改用户基本信息"""
    def change_user_info(self, new_name, new_motto,  token):
        url = "http://47.103.131.3:7943/myauth/soft/editInfo"
        data = {
            "device_info": self.device_info,
            "device_code": self.device_code,
            "newName": new_name,
            "newQq": new_motto,
            "token": token,
            "timestamp": str(time.time())[:10]
        }
        payload = json.dumps({
            "data": data,
            "skey": self.skey,
            "vkey": self.vkey,
            "sign": self.get_sign(data)
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        return response.json()

    """心跳包"""
    def heartbeat(self, token):
        url = "http://47.103.131.3:7943/myauth/soft/heart"
        data = {
            "device_info": self.device_info,
            "device_code": self.device_code,
            "token": token,
            "timestamp": str(time.time())[:10]
        }
        payload = json.dumps({
            "data": data,
            "skey": self.skey,
            "vkey": self.vkey,
            "sign": self.get_sign(data)
        })

        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.json()["msg"])

    """获得用户机器码"""
    @staticmethod
    def get_machine_code():
        serial_number = []
        machine_code = ""
        c = wmi.WMI()
        for board in c.Win32_BaseBoard():
            serial_number.append(board.SerialNumber)
            break
        for disk in c.Win32_DiskDrive():
            serial_number.append(disk.Model)
            break
        for cpu in c.Win32_Processor():
            serial_number.append(cpu.ProcessorId)
            break
        for code in serial_number:
            machine_code = machine_code + code.replace(" ", "")
        return machine_code
