"""
用于客户端Consumer到注册中心的连接器
"""
import json
import socket
from time import sleep as time_sleep
from eqlink.components.remote_server import remote_server
import traceback

'''失效服务列表'''
fail_server_list = []


class LinkClient:
    def __init__(self, server_conf, client_conf):
        """
        初始化
        :param server_conf: 注册中心配置
        :param client_conf: Consumer客户端配置
        """
        self.server_conf = server_conf
        self.client_conf = client_conf

    def client_int(self, data_to_server):
        """
        客户端 socket 初始化
        :param data_to_server: 发送到注册中心的数据
        :return: void
        """
        client = None
        try:
            ''' 创建socket套接字 '''
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[eqlink] Error creating socket: %s" + str(e))
            print(traceback.format_exc())

        try:
            '''  服务端的IP地址和端口 '''
            client.connect((self.server_conf['IP'], self.server_conf['PORT']))
            '''
            setblocking(flag):
                如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。
                非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。
            --- code ---
            client.setblocking(False)
            '''
            print(f"[eqlink] connect link server success on {self.server_conf['IP']}:{self.server_conf['PORT']}")
        except socket.error as e:
            print('[eqlink] connected to link center error: %s' + str(e))
            print(traceback.format_exc())
            return 'connect fail'

        ''' 与注册中心保持连接，定时获取服务列表 '''
        while True:
            data_json = json.dumps(data_to_server)
            # print('[consumer]', data_to_server)
            if len(data_to_server['fail_server']) == 0:
                fail_server_flag = False
            else:
                fail_server_flag = True
            try:
                client.sendall(bytes(data_json, encoding="utf8"))
                data = client.recv(self.server_conf['BUF_SIZE'])
                ''' 注册中心服务列表写入共享存储区 '''
                remote_server.__set__(json.loads(data))
                if fail_server_flag:
                    data_to_server['fail_server'] = []
                # print('[eqlink] [获取Provider服务列表]:', str(data, 'UTF-8'))  # 连接成功不进行控制台打印（日志太多）
            except socket.error as e:
                print('[eqlink] consumer get provider list send failed: ', e)
                print(traceback.format_exc())
                break
            ''' 间隔一段时间，进行一次心跳检擦，心跳数据设置 '''
            time_sleep(self.client_conf['alive'])
        return 'send fail'
