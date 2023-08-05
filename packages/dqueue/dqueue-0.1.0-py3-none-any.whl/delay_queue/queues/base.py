# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from threading import RLock

from runners import BackgroundRunner, TIMEOUT_MIN
from storages.base import BaseStorage
from storages.redis import RedisStorage
from storages.memory import MemoryStorage


class BaseQueue(ABC):
    # TODO: 未来自动引入，暂时手动
    _storage_classes = {
        'redis': RedisStorage,
        'memory': MemoryStorage
    }

    def __init__(self):
        self._storages = {}
        self._storages_lock = self._create_lock()
        self._runner = None

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def push(self, item):
        ...

    def add(self, item, ttl, storage='default'):
        storage: BaseStorage = self._lookup_storage(storage)
        storage.add_item(item, ttl)

    def _lookup_storage(self, alias):
        try:
            return self._storages[alias]
        except KeyError:
            raise KeyError('No lookup storage: %s' % alias)

    def _process(self):
        now = datetime.now()
        with self._storages_lock:
            for storage_alias, storage in self._storages.items():
                due_items = storage.get_due_items(now)
                for item in due_items:
                    self.push(item)
                    storage.remove_item(item)
        return TIMEOUT_MIN

    def add_storage(self, storage, alias='default', **options):

        if isinstance(storage, BaseStorage):
            self._storages[alias] = storage
        elif isinstance(storage, str):
            self._storages[alias] = self._create_plugin_instance(storage, options)
        else:
            raise TypeError('storage must be BaseStorage or str')

        self._runner.wakeup()

    def _create_plugin_instance(self, alias, options):
        class_container, base_class = (self._storage_classes, BaseStorage)
        plugin_cls = class_container[alias]
        return plugin_cls(**options)

    def start(self, paused=False):
        self._runner = self._create_default_runner()
        self._runner.start(self)

        with self._storages_lock:
            if 'default' not in self._storages:
                self.add_storage(self._create_default_storage(), 'default')

            for alias, storage in self._storages.items():
                storage.start(self, alias)

        if not paused:
            self._runner.wakeup()

    def _create_lock(self): # noqa
        return RLock()

    def _create_default_storage(self):  # noqa
        return MemoryStorage()

    def _create_default_runner(self):  # noqa
        return BackgroundRunner()

    @abstractmethod
    def shutdown(self):
        for storage in self._storages.values():
            storage.shutdown()
        self._runner.shutdown()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
