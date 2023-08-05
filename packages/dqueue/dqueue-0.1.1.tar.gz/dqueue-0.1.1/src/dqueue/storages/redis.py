# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from dataclasses import asdict

from redis import Redis

from dqueue.exceptions import ItemExistError, ItemKeyError
from dqueue.item import Item
from dqueue.storages.base import BaseStorage
from dqueue.utils import after_timestamp, datetime_to_timestamp


class RedisStorage(BaseStorage):

    def __init__(self, db=0, queue_key="delay:queue", due_times_key="delay:due_times", **connect_args):
        self.queue_key = queue_key
        self.due_times_key = due_times_key
        self.redis = Redis(db=int(db), **connect_args)

    def get_due_items(self, now):
        now_timestamp = datetime_to_timestamp(now)
        ids = self.redis.zrangebyscore(self.due_times_key, 0, now_timestamp)
        if ids:
            states = self.redis.hmget(self.queue_key, *ids)
            return [Item(**json.loads(state)) for state in states]
        return []

    def get_all_items(self):
        states = self.redis.hgetall(self.queue_key)
        return [Item(**json.loads(v)) for k, v in states.items()]

    def add_item(self, item: Item, ttl):
        if self.redis.hexists(self.queue_key, item.id):
            raise ItemExistError(item.id)

        with self.redis.pipeline() as pipe:
            pipe.multi()
            pipe.hset(self.queue_key, item.id, json.dumps(asdict(item)))
            pipe.zadd(self.due_times_key, {item.id: after_timestamp(ttl)})
            pipe.execute()

    def remove_item(self, item):
        item_id = item if not isinstance(item, Item) else item.id
        if not self.redis.hexists(self.queue_key, item_id):
            raise ItemKeyError(item_id)

        with self.redis.pipeline() as pipe:
            pipe.hdel(self.queue_key, item_id)
            pipe.zrem(self.due_times_key, item_id)
            pipe.execute()

    def remove_all_items(self):
        with self.redis.pipeline() as pipe:
            pipe.delete(self.queue_key)
            pipe.delete(self.due_times_key)
            pipe.execute()

    def shutdown(self):
        self.redis.connection_pool.disconnect()
