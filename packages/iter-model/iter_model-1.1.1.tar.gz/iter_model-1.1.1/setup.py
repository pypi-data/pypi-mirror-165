# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iter_model']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iter-model',
    'version': '1.1.1',
    'description': 'iter-model uses a method approach instead of individual functions to work with iterable objects.',
    'long_description': '# Iter Model\n\n<a href="https://pypi.org/project/iter_model" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/iter_model.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n<a href="https://pypi.org/project/iter_model" target="_blank">\n    <img src="https://img.shields.io/pypi/v/iter_model?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://github.com/VolodymyrBor/iter_model/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">\n    <img src="https://github.com/VolodymyrBor/iter_model/workflows/Test/badge.svg?event=push&branch=master" alt="Test">\n</a>\n\n[![Supported Versions](https://img.shields.io/badge/coverage-100%25-green)](https://shields.io/)\n[![Supported Versions](https://img.shields.io/badge/poetry-✅-grey)](https://shields.io/)\n[![Supported Versions](https://img.shields.io/badge/async-✅-grey)](https://shields.io/)\n[![Supported Versions](https://img.shields.io/badge/mypy-✅-grey)](https://shields.io/)\n\n## Description\n\n**Iter Model** uses a method approach instead of individual functions to work with iterable objects.\n\n### Native approach\n\n```python\nresult = list(map(\n    lambda x: x ** 2,\n    filter(lambda x: x % 2 == 0, range(10)),\n))\n```\n\n### Iter Model approach\n\n```python\nfrom iter_model import SyncIter\n\nresult = (\n    SyncIter(range(10))\n        .where(lambda x: x % 2 == 0)\n        .map(lambda x: x ** 2)\n        .to_list()\n)\n\n```\n\n### Generators\n\nYou can decorate your generator function and get SyncIter as a result\n\n```python\nfrom iter_model import sync_iter\n\n\n@sync_iter\ndef some_generator():\n    for item in range(10):\n        yield item\n\n\nresult = some_generator().take_while(lambda x: x < 5).to_list()\n```\n\n### Async support\n\nIter Model also support async iterable and async function as condition.\n\n\n```python\nimport asyncio\n\nfrom iter_model import async_iter\n\n\n@async_iter\nasync def some_generator():\n    for item in range(10):\n        yield item\n\n        \nasync def condition_a(x):\n    """Some async condition"""\n    return x % 2 == 0 \n\n\ndef condition_b(x):\n    """Some sync condition"""\n    return x > 5 \n\n\nasync def main():\n    result = await (\n        some_generator()\n            .where(condition_a)\n            .take_while(condition_b)\n            .to_list()\n    )\n    print(result)\n    \n\n\nasyncio.run(main())\n```\n\n### SyncIter/AsyncIter provide the following methods\n\n- ```to_list()```\n- ```to_tuple()```\n- ```to_set()```\n- ```enumerate()```\n- ```take()```\n- ```map()```\n- ```skip()```\n- ```skip_while()```\n- ```count()```\n- ```first_where()```\n- ```where()```\n- ```take_while()```\n- ```first()```\n- ```last()```\n- ```chain()```\n- ```all()```\n- ```any()```\n- ```first()```\n- ```mark_first()```\n- ```mark_last()```\n- ```mark_first_last()```\n- ```reduce()```\n- ```max()```\n- ```min()```\n- ```accumulate()```\n- ```append_left()```\n- ```append_right()```\n- ```append_at()```\n- ```zip()```\n- ```zip_longest()```\n- ```slice()```\n',
    'author': 'volodymyrb',
    'author_email': 'volodymyr.borysiuk0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VolodymyrBor/iter_model',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
