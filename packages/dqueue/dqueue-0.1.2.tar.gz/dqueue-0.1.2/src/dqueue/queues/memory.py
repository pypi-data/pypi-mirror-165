# -*- coding: utf-8 -*-
from queue import Queue, Empty
from typing import Union

from dqueue.queues.base import BaseQueue


class MemoryQueue(BaseQueue):
    def __init__(self):
        super().__init__()
        self.q = Queue()
        self.start()

    def _get(self, block: Union[bool, int] = True):
        _block = True
        _timeout = None
        if isinstance(block, bool):
            _block = block
        elif isinstance(block, int):
            _block = True
            _timeout = block
        else:
            raise ValueError("block must be bool or int")

        try:
            return self.q.get(block=_block, timeout=_timeout)
        except Empty:
            return None

    def get(self, count=1, block: Union[bool, int] = True):
        for _ in range(count):
            item = self._get(block=block)
            if item is None:
                break
            yield item

    def push(self, item):
        self.q.put(item)

    def shutdown(self):
        super(MemoryQueue, self).shutdown()
