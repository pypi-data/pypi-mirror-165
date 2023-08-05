"""
Provider服务到注册中心的注册器
"""
import json
import socket
from sys import exit as sys_exit


class LinkRegister:
    def __init__(self, server_conf):
        """
        初始化
        :param server_conf: 注册中心配置
        """
        self.server_conf = server_conf

    def register_int(self, send_data):
        """
        服务提供者注册
        :return: None
        """
        register = None
        try:
            register = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[eqlink] [Provider Socket创建] [ERROR]: " + str(e))
            sys_exit()
        try:
            register.connect((self.server_conf['IP'], self.server_conf['PORT']))
            ''' register.setblocking(False) # 设置非阻塞模式 '''
            print('[eqlink] [连接注册中心] [SUCCESS] IP:' + self.server_conf['IP'])
        except socket.gaierror as e:
            print("[eqlink] [连接注册中心] [ERROR]: " + str(e))
            sys_exit()
        '''发送信息到注册中心'''
        try:
            register.sendall(bytes(json.dumps(send_data), encoding="utf8"))
            print("[eqlink] [Provider注册] [register data]:", json.dumps(send_data))
            data = register.recv(self.server_conf['BUF_SIZE'])
            print('[eqlink] [Provider注册] [response]:', str(data, 'UTF-8'))
        except socket.error as e:
            print("[eqlink] [Provider注册] [error]: " + str(e))
            sys_exit()
        ''' 关闭注册连接 '''
        register.close()
