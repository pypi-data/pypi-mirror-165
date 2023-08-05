# -*- coding: utf-8 -*-
from dqueue.exceptions import ItemExistError, ItemKeyError
from dqueue.item import Item
from dqueue.storages.base import BaseStorage
from dqueue.utils import after_timestamp, datetime_to_timestamp


class MemoryStorage(BaseStorage):

    def __init__(self):
        self._items = []
        self._item_index = {}

    def get_due_items(self, now):
        now_timestamp = datetime_to_timestamp(now)
        return [
            item
            for item, timestamp in self._items
            if timestamp and timestamp <= now_timestamp
        ]

    def get_all_items(self):
        return [item[0] for item in self._items]

    def add_item(self, item: Item, ttl):
        if item.id in self._item_index:
            raise ItemExistError(item.id)
        timestamp = after_timestamp(ttl)
        index = self._get_item_index(timestamp, item.id)
        self._items.insert(index, (item, timestamp))
        self._item_index[item.id] = (item, timestamp)

    def remove_item(self, item):
        item_id = item if not isinstance(item, Item) else item.id

        item, timestamp = self._item_index.get(item_id, (None, None))
        if item is None:
            raise ItemKeyError(item_id)
        index = self._get_item_index(timestamp, item_id)
        del self._items[index]
        del self._item_index[item_id]

    def remove_all_items(self):
        self._items = []
        self._item_index = {}

    def shutdown(self):
        self.remove_all_items()

    def _get_item_index(self, timestamp, job_id):
        """二分查找法"""
        lo, hi = 0, len(self._items)
        timestamp = float('inf') if timestamp is None else timestamp
        while lo < hi:
            mid = (lo + hi) // 2
            mid_job, mid_timestamp = self._items[mid]
            mid_timestamp = float('inf') if mid_timestamp is None else mid_timestamp
            if mid_timestamp > timestamp:
                hi = mid
            elif mid_timestamp < timestamp:
                lo = mid + 1
            elif mid_job.id > job_id:
                hi = mid
            elif mid_job.id < job_id:
                lo = mid + 1
            else:
                return mid

        return lo
