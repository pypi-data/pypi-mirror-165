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
    'version': '0.1.1',
    'description': 'python通用延迟消息队列',
    'long_description': '# delay_queue\n\nWarning！！！',
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
