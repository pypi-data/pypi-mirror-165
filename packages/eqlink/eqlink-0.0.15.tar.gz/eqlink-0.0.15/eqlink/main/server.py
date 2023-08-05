"""
注册中心本地服务实现
"""

import socket
import sys
from threading import Thread
from eqlink.components.protocol import *


def not_c_key(p_dict, p_key):
    """
    判断不包含元素
    :param p_dict: 字典
    :param p_key: key
    :return: p_dict 不包含 p_key, 返回 True
    """
    try:
        if p_dict.__contains__(p_key) is True and p_dict[p_key] is not None and p_dict[p_key] != '':
            return False
    except Exception as e:
        print('[eqlink]', 'conf check', str(e))
    return True


class LinkServer:
    def __init__(self, server_conf, local_storage_path):
        self.server_conf = {}
        self.storage_path = local_storage_path
        self.server_conf['HOST'] = '127.0.0.1' if not_c_key(server_conf, 'HOST') else server_conf['HOST']
        self.server_conf['PORT'] = 7900 if not_c_key(server_conf, 'PORT') else server_conf['PORT']
        self.server_conf['BACKLOG'] = 5 if not_c_key(server_conf, 'BACKLOG') else server_conf['BACKLOG']
        self.server_conf['BUF_SIZE'] = 1024 if not_c_key(server_conf, 'BUF_SIZE') else server_conf['BUF_SIZE']

    def __data_recv__(self, c_connect):
        """
        等待客户端请求
        :param c_connect: socket 连接
        :return: void
        """
        while True:
            '''处理客户端端数据'''
            try:
                """
                recv(buffer_size) 接收TCP数据，数据以字符串形式返回，buffer_size 指定要接收的最大数据量
                """
                data = c_connect.recv(self.server_conf['BUF_SIZE'])
                data = str(data, 'UTF-8')
                ''' 客户端发送空内容，关闭连接 '''
                if data == '':
                    break
                ''' 解析客户端请求，不同类型的请求，进行不同的处理 '''
                data_json = json.loads(data)
                response = protocol_analysis(data_json, self.storage_path)
                ''' 响应客户端请求 '''
                c_connect.sendall(bytes(json.dumps(response).encode('utf-8')))
            except socket.error as e:
                print('[eqlink] [Socket Error]', str(e))
                break
        '''关闭客户端连接'''
        c_connect.close()

    def server_init(self):
        """
        服务端 socket 初始化
        :return: None
        """
        try:
            ''' 创建Socket套接字 '''
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print('[eqlink] [注册中心 socket] [初始化异常] ' + str(e))
            sys.exit()

        try:
            ''' 绑定本地端口 主机地址 '''
            server.bind((self.server_conf['HOST'], self.server_conf['PORT']))
            print('[eqlink] 注册中心绑定 ' + self.server_conf['HOST'] + ':' + str(self.server_conf['PORT']))
        except socket.error as e:
            print("[eqlink] Bind failed!" + str(e))
            sys.exit()

        """
        服务启动 listen(backlog) 开始TCP监听
        backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5即可
        """
        server.listen(self.server_conf['BACKLOG'])
        print("[eqlink] 初始化已完成 Waiting for connection")

        ''' 加载本地存储的服务 '''
        try:
            f = open(self.storage_path, "r", encoding="utf-8")
            server_list = f.read()
            link_list.provider_list = json.loads(server_list)
            print('[eqlink] 加载本地服务', link_list.provider_list)
        except Exception as e:
            print('[eqlink] 本地服务加载失败', e)

        while True:
            ''' accept() 被动接受TCP客户端连接，(阻塞式)等待连接的到来 '''
            connect, addr = server.accept()
            print("[eqlink] Connected with %s:%s " % (addr[0], str(addr[1])))
            ''' 有客户都端连接后，另启动一个线程 '''
            Thread(target=self.__data_recv__, args=(connect,)).start()
