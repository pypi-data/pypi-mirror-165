# -*- coding: utf-8 -*-
"""
RabbitMQ 延迟队列需要自行安装插件：
>> https://github.com/rabbitmq/rabbitmq-delayed-message-exchange

RabbitMQ 延迟队列使用教程：
@see https://52caiji.com/posts/other/rabbitmq-delay-queue.html
"""
import json
from dataclasses import asdict
from typing import Union, List

from amqpstorm import Connection, Message

from dqueue.queues.base import BaseQueue


class RabbitMQQueue(BaseQueue):
    def __init__(self,
                 exchange_name="delayed.exchange",
                 queue_name="delayed.queue",
                 routing_key="delayed.routing.key",
                 hostname="localhost",
                 username="guest",
                 password="guest",
                 **connect_args):
        super().__init__()
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.conn = Connection(hostname, username, password, **connect_args)
        self.channel = self.conn.channel()

        self._configuration()

    def _configuration(self):
        arguments = {"x-delayed-type": "direct"}
        self.channel.exchange.declare(self.exchange_name,
                                      exchange_type="x-delayed-message",  # plugin support
                                      durable=True,
                                      arguments=arguments)
        self.channel.queue.declare(self.queue_name, durable=True)
        self.channel.queue.bind(
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key,
        )

    def add(self, item, ttl, storage='default'):
        self.channel.basic.publish(
            json.dumps(asdict(item)),
            self.routing_key,
            self.exchange_name,
            properties={'headers': {"x-delay": ttl}}
        )

    def get(self, count=1, *args, **kwargs) -> List[Union[Message, None]]:
        messages = []
        for _ in range(count):
            message = self.channel.basic.get(self.queue_name, *args, **kwargs)
            if not message:
                continue
            messages.append(message)
        return messages

    def push(self, item): ...

    def ack(self, message):
        if isinstance(message, Message):
            message.ack()
        elif isinstance(message, int):
            self.channel.basic.ack(delivery_tag=message)
        else:
            raise ValueError("message must be Message or int")

    def shutdown(self):
        super(RabbitMQQueue, self).shutdown()
        self.channel.close()
        self.conn.close()
