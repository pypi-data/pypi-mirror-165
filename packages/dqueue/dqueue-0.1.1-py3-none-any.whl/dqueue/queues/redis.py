# -*- coding: utf-8 -*-
"""
基于Redis的延迟队列

    基于Redis的延迟队列，可以将任务放入队列，并且可以设置延迟时间，当达到延迟时间时，任务将被取出。
    本模式是采用Redis的Stream实现，因此在使用本模式前，必须达到的基本要求是Redis的版本应该是5.x及以上。

"""
from __future__ import absolute_import
from dataclasses import asdict
from typing import Union

from redis import Redis

from dqueue.queues.base import BaseQueue


class RedisQueue(BaseQueue):
    def __init__(self, db=0, group_key="default_group", queue_key="delay:stream", streamId="0", **connect_args):
        super().__init__()
        self.group_key = group_key
        self.queue_key = queue_key
        self.streamId = streamId
        self.redis = Redis(db=int(db), **connect_args)

        self._create_xgroup()
        self.start()

    def _create_xgroup(self):
        try:
            self.redis.xgroup_create(self.queue_key, self.group_key, id=self.streamId, mkstream=True)
        except:
            pass

    def push(self, item):
        self.redis.xadd(self.queue_key, asdict(item))

    def get(self, count=1, consumer="default", streamId=">", block=None):
        """
        Read from a stream via a consumer group;
        :param count: if set, only return this many items, beginning with the
               earliest available;
        :param consumer: name of the requesting consumer;
        :param streamId: IDs indicate the last ID already seen;
        :param block: number of milliseconds to wait, if nothing already present.
        :return:
        """
        res = self.redis.xreadgroup(self.group_key, consumer, {self.queue_key: streamId}, count=count, block=block)
        if not res:
            return []
        [[_, messages]] = res
        return messages

    def ack(self, message: Union[list, tuple, bytes, str]):
        if not len(message):
            return
        if isinstance(message, (bytes, str)):
            ids = [message]
        elif isinstance(message, list):
            ids = [msg_id for msg_id, _ in message]
        elif isinstance(message, tuple):
            ids = [message[0]]
        else:
            raise TypeError("message must be bytes, str, list or tuple")
        self.redis.xack(self.queue_key, self.group_key, *ids)

    def shutdown(self):
        super(RedisQueue, self).shutdown()
        self.redis.connection_pool.disconnect()