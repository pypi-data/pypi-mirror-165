# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskiq_aio_pika', 'taskiq_aio_pika.tests']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=8.1.0,<9.0.0', 'taskiq>=0,<1']

setup_kwargs = {
    'name': 'taskiq-aio-pika',
    'version': '0.0.6',
    'description': 'RabbitMQ broker for taskiq',
    'long_description': '# AioPika broker for taskiq\n\nThis lirary provides you with aio-pika broker for taskiq.\n\nUsage:\n```python\nfrom taskiq_aio_pika import AioPikaBroker\n\nbroker = AioPikaBroker()\n\n@broker.task\nasync def test() -> None:\n    print("nothing")\n\n```\n\n## Non-obvious things\n\nYou can send delayed messages and set priorities to messages using labels.\n\n## Delays\n\nTo send delayed message, you have to specify\ndelay label. You can do it with `task` decorator,\nor by using kicker. For example:\n\n```python\nbroker = AioPikaBroker()\n\n@broker.task(delay=3)\nasync def delayed_task() -> int:\n    return 1\n\nasync def main():\n    await broker.startup()\n    # This message will be received by workers\n    # After 3 seconds delay.\n    await delayed_task.kiq()\n\n    # This message is going to be received after the delay in 4 seconds.\n    # Since we overriden the `delay` label using kicker.\n    await delayed_task.kicker().with_labels(delay=4).kiq()\n\n    # This message is going to be send immediately. Since we deleted the label.\n    await delayed_task.kicker().with_labels(delay=None).kiq()\n\n    # Of course the delay is managed by rabbitmq, so you don\'t\n    # have to wait delay period before message is going to be sent.\n```\n\n\n## Priorities\n\nYou can define priorities for messages using `priority` label.\nMessages with higher priorities are delivered faster.\nBut to use priorities you need to define `max_priority` of the main queue, by passing `max_priority` parameter in broker\'s init.\nThis parameter sets maximum priority for the queue and\ndeclares it as the prority queue.\n\nBefore doing so please read the [documentation](https://www.rabbitmq.com/priority.html#behaviour) about what\ndownsides you get by using prioritized queues.\n\n\n```python\nbroker = AioPikaBroker(max_priority=10)\n\n# We can define default priority for tasks.\n@broker.task(priority=2)\nasync def prio_task() -> int:\n    return 1\n\nasync def main():\n    await broker.startup()\n    # This message has priority = 2.\n    await prio_task.kiq()\n\n    # This message is going to have priority 4.\n    await prio_task.kicker().with_labels(priority=4).kiq()\n\n    # This message is going to have priority 0.\n    await prio_task.kicker().with_labels(priority=None).kiq()\n\n```\n\n## Configuration\n\nAioPikaBroker parameters:\n* `url` - url to rabbitmq. If None, "amqp://guest:guest@localhost:5672" is used.\n* `result_backend` - custom result backend.\n* `task_id_generator` - custom task_id genertaor.\n* `exchange_name` - name of exchange that used to send messages.\n* `exchange_type` - type of the exchange. Used only if `declare_exchange` is True.\n* `queue_name` - queue that used to get incoming messages.\n* `routing_key` - that used to bind that queue to the exchange.\n* `declare_exchange` - whether you want to declare new exchange if it doesn\'t exist.\n* `max_priority` - maximum priority for messages.\n* `delay_queue_name` - custom delay queue name.\n    This queue is used to deliver messages with delays.\n* `dead_letter_queue_name` - custom dead letter queue name.\n    This queue is used to receive negatively acknowleged messages from the main queue.\n* `qos` - number of messages that worker can prefetch.\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taskiq-python/taskiq-aio-pika',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
