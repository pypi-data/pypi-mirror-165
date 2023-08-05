# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dqueue', 'dqueue.queues', 'dqueue.storages']

package_data = \
{'': ['*']}

install_requires = \
['AMQPStorm>=2.10.5,<3.0.0', 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'dqueue',
    'version': '0.1.2',
    'description': 'python通用延迟消息队列',
    'long_description': "\n## Usage\n\n> pip install dqueue\n\n## Example\n### Memory Queue\n\n```python\n# memory queue\nimport threading\n\nfrom dqueue.queues import MemoryQueue\nfrom dqueue.item import Item\n\nqueue = MemoryQueue()\n\n# 模拟不同延迟发布消息\ndef publisher():\n    for i in range(10):\n        item = Item(data=f'hello {i}')\n        queue.add(item, i * 1000)\n\n# 模拟消费端取延迟消息\ndef consumer():\n    while True:\n        messages = queue.get(block=10 * 1000)\n        for msg in messages:\n            print('message:', msg)\n\n\nthreading.Thread(target=publisher).start()\nthreading.Thread(target=consumer).start()\n```\n\n### Redis Queue\n\nYou can continue with the example above and Just change the declare.\n\n```python\nfrom dqueue.queues import RedisQueue\n\nqueue = RedisQueue()\n\n# same code\n```",
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mic1on/delay_queue',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
