"""
用于存储服务消费者和提供者列表
"""


class LinkList:
    def __init__(self):
        """
        provider_list: 服务提供者列表
        provider_list: 服务提供者列表 备份的目录
        consumer_list: TODO 服务消费者连接列表
        """
        self.provider_list = {}
        self.provider_list_backup = {}
        self.consumer_list = {}

    def add_provider(self, provider):
        """
        将服务提供者加入到注册中心本地
        :param provider: 服务提供者信息
        :return: void
        """
        service_name = provider['service_name']
        if service_name in self.provider_list:
            '''服务已注册，对比是否增加服务可调用IP或方法'''
            if 'remote' in self.provider_list[service_name]:
                ''' 遍历服务列表，服务存在时，调整权重 '''
                for item in self.provider_list[service_name]['remote']:
                    if item['ip'] == provider['remote']['ip'] and item['port'] == provider['remote']['port']:
                        item['weight'] = provider['remote']['weight']
                '''如果服务不在列表，则添加'''
                if provider['remote'] not in self.provider_list[service_name]['remote']:
                    self.provider_list[service_name]['remote'].append(provider['remote'])
                '''调整服务的方法列表'''
                self.provider_list[service_name]['func'] = provider['func']
        else:
            '''首次进行服务注册'''
            self.provider_list[service_name] = {
                'remote': [provider['remote']],
                'func': provider['func']
            }
