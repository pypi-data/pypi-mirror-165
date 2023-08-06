# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskiq_redis', 'taskiq_redis.tests']

package_data = \
{'': ['*']}

install_requires = \
['redis>=4.2.0,<5.0.0', 'taskiq>=0,<1']

setup_kwargs = {
    'name': 'taskiq-redis',
    'version': '0.0.4',
    'description': 'Redis integration for taskiq',
    'long_description': '# TaskIQ-Redis\n\nTaskiq-redis is a plugin for taskiq that adds a new broker and result backend based on redis.\n\n# Installation\n\nTo use this project you must have installed core taskiq library:\n```bash\npip install taskiq\n```\nThis project can be installed using pip:\n```bash\npip install taskiq-redis\n```\n\n# Usage\n\nLet\'s see the example with the redis broker and redis async result:\n```python\nimport asyncio\n\nfrom taskiq_redis.redis_broker import RedisBroker\nfrom taskiq_redis.redis_backend import RedisAsyncResultBackend\n\n\nredis_async_result = RedisAsyncResultBackend(\n    url="redis://localhost:6379",\n)\n\nbroker = RedisBroker(\n    url="redis://localhost:6379",\n    result_backend=redis_async_result,\n)\n\n\n@broker.task\nasync def best_task_ever() -> None:\n    """Solve all problems in the world."""\n    await asyncio.sleep(5.5)\n    print("All problems are solved!")\n\n\nasync def main():\n    task = await my_async_task.kiq()\n    print(await task.get_result())\n\n\nasyncio.run(main())\n```\n\n## RedisBroker configuration\n\nRedisBroker parameters:\n* `url` - url to redis.\n* `task_id_generator` - custom task_id genertaor.\n* `result_backend` - custom result backend.\n* `queue_name` - name of the pub/sub channel in redis.\n* `max_connection_pool_size` - maximum number of connections in pool.\n\n## RedisAsyncResultBackend configuration\n\nRedisAsyncResultBackend parameters:\n* `url` - url to redis.\n',
    'author': 'taskiq-team',
    'author_email': 'taskiq@norely.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taskiq-python/taskiq-redis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
