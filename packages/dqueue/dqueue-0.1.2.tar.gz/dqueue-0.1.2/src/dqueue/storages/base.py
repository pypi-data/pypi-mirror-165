# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def get_due_items(self, now):
        """
        返回到期的数据
        :return: list[item]
        """

    @abstractmethod
    def get_all_items(self):
        """
        返回数据库中的所有数据
        :return: list[item]
        """

    @abstractmethod
    def add_item(self, item, ttl):
        """
        添加数据
        :param item: Item Data
        :param ttl: 毫秒 过期时间
        :return:
        """

    @abstractmethod
    def remove_item(self, item):
        """
        删除数据
        :param item: Item Data
        :return:
        """

    @abstractmethod
    def remove_all_items(self):
        """
        删除数据库中所有的数据
        :return:
        """

    def shutdown(self):
        """用于释放资源"""

    def start(self, *args, **kwargs): ...

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
