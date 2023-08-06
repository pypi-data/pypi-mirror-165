# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskiq_pipelines', 'taskiq_pipelines.steps', 'taskiq_pipelines.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.2,<2.0.0',
 'taskiq>=0.0.8,<1',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'taskiq-pipelines',
    'version': '0.0.2',
    'description': 'Taskiq pipelines for task chaining.',
    'long_description': '# Pipelines for taskiq\n\nTaskiq pipelines is a `fire-and-forget` at its limit.\n\nImagine you have a really tough functions and you want\nto call them sequentially one after one, but you don\'t want to wait for them\nto complete. taskiq-pipeline solves this for you.\n\n## Installation\n\n\nYou can install it from pypi:\n```\npip install taskiq-pipelines\n```\n\nAfter you installed it you need to add our super clever middleware\nto your broker.\n\nThis middleware actually decides what to do next, after current step\nis completed.\n\n```python\nfrom taskiq_pipelines.middleware import PipelineMiddleware\n\nmy_super_broker = ...\n\n\nmy_super_broker.add_middlewares(\n    [\n        PipelineMiddleware(),\n    ]\n)\n```\n\nAlso we have to admit that your broker MUST use result_backend that\ncan be read by all your workers. Pipelines work with inmemorybroker,\nfeel free to use it in local development.\n\n\n### Example\n\nFor this example I\'m going to use one single script file.\n\n```python\nimport asyncio\nfrom typing import Any, List\nfrom taskiq.brokers.inmemory_broker import InMemoryBroker\nfrom taskiq_pipelines import PipelineMiddleware, Pipeline\n\nbroker = InMemoryBroker()\nbroker.add_middlewares([PipelineMiddleware()])\n\n\n@broker.task\ndef add_one(value: int) -> int:\n    return value + 1\n\n\n@broker.task\ndef repeat(value: Any, reps: int) -> List[Any]:\n    return [value] * reps\n\n\n@broker.task\ndef check(value: int) -> bool:\n    return value >= 0\n\n\nasync def main():\n    pipe = (\n        Pipeline(\n            broker,\n            add_one,  # First of all we call add_one function.\n        )\n        # 2\n        .call_next(repeat, reps=4)  #  Here we repeat our value 4 times\n        # [2, 2, 2, 2]\n        .map(add_one)  # Here we execute given function for each value.\n        # [3, 3, 3, 3]\n        .filter(check)  # Here we filter some values.\n        # But sice our filter filters out all numbers less than zero,\n        # our value won\'t change.\n        # [3, 3, 3, 3]\n    )\n    task = await pipe.kiq(1)\n    result = await task.wait_result()\n    print("Calculated value:", result.return_value)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\nIf you run this example, it prints this:\n```bash\n$ python script.py\nCalculated value: [3, 3, 3, 3]\n```\n\nLet\'s talk about this example.\nTwo notable things here:\n1. We must add PipelineMiddleware in the list of our middlewares.\n2. We can use only tasks as functions we wan to execute in pipeline.\n    If you want to execute ordinary python function - you must wrap it in task.\n\nPipeline itself is just a convinient wrapper over list of steps.\nConstructed pipeline has the same semantics as the ordinary task, and you can add steps\nmanually. But all steps of the pipeline must implement `taskiq_pipelines.abc.AbstractStep` class.\n\nPipelines can be serialized to strings with `dumps` method, and you can load them back with `Pipeline.loads` method. So you can share pipelines you want to execute as simple strings.\n\nPipeline assign `task_id` for each task when you call `kiq`, and executes every step with pre-calculated `task_id`,\nso you know all task ids after you call kiq method.\n\n\n## How does it work?\n\nAfter you call `kiq` method of the pipeline it pre-calculates\nall task_ids, serializes itself and adds serialized string to\nthe labels of the first task in the chain.\n\nAll the magic happens in the middleware.\nAfter task is executed and result is saved, you can easily deserialize pipeline\nback and calculate pipeline\'s next move. And that\'s the trick.\nYou can get more information from the source code of each pipeline step.\n\n# Available steps\n\nWe have a few steps available for chaining calls:\n1. Sequential\n2. Mapper\n3. Filter\n\n### Sequential steps\n\nThis type of step is just an ordinary call of the function.\nIf you haven\'t specified `param_name` argument, then the result\nof the previous step will be passed as the first argument of the function.\nUf you did specify the `param_name` argument, then the result of the previous\nstep can be found in key word arguments with the param name you specified.\n\nYou can add sequential steps with `.call_next` method of the pipeline.\n\n### Mapper step\n\nThis step runs specified task for each item of the previous task\'s result spawning\nmultiple tasks.\nBut I have to admit, that the result of the previous task must be iterable.\nOtherwise it will mark the pipeline as failed.\n\nAfter the execution you\'ll have mapped list.\nYou can add mappers by calling `.map` method of the pipeline.\n\n### Filter step\n\nThis step runs specified task for each item of the previous task\'s result.\nBut I have to admit, that the result of the previous task must be iterable.\nOtherwise it will mark the pipeline as failed.\n\nIf called tasks returned `True` for some element, this element will be added in the final list.\n\nAfter the execution you\'ll get a list with filtered results.\nYou can add filters by calling `.filter` method of the pipeline.\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taskiq-python/taskiq-pipelines',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
