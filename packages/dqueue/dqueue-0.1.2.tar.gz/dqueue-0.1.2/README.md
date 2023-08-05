
## Usage

> pip install dqueue

## Example
### Memory Queue

```python
# memory queue
import threading

from dqueue.queues import MemoryQueue
from dqueue.item import Item

queue = MemoryQueue()

# 模拟不同延迟发布消息
def publisher():
    for i in range(10):
        item = Item(data=f'hello {i}')
        queue.add(item, i * 1000)

# 模拟消费端取延迟消息
def consumer():
    while True:
        messages = queue.get(block=10 * 1000)
        for msg in messages:
            print('message:', msg)


threading.Thread(target=publisher).start()
threading.Thread(target=consumer).start()
```

### Redis Queue

You can continue with the example above and Just change the declare.

```python
from dqueue.queues import RedisQueue

queue = RedisQueue()

# same code
```