"""
子模块读取工具
"""
from importlib import import_module
from sys import path as sys_path


class ReadModule:
    def __init__(self, path=None):
        """
        初始化
        :param path: 要读取的子模块所在路径
        """
        if path is None:
            path = '..'
        sys_path.append(path)
        self.module_list = {}

    def read(self, item):
        """
        要读取的子模块
        :param item: 子模块名称
        :return: 子模块
        """
        if item in self.module_list.keys():
            '''相同的子模块如果已读取，直接返回'''
            return self.module_list[item]
        '''子模块导入'''
        module_item = import_module(item)
        self.module_list[item] = module_item
        return module_item
