# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cacha', 'cacha.store', 'cacha.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0', 'pandas>=1.4.3,<2.0.0', 'pickleDB>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'cacha',
    'version': '1.0.0',
    'description': 'A simple cache context manager for Data Scientists.',
    'long_description': '## Cacha\n\n---\n\n[![CI/CD](https://github.com/smolendawid/cacha/actions/workflows/cicd.yaml/badge.svg)](https://github.com/smolendawid/cacha/actions/workflows/cicd.yaml)\n[![PyPi](https://img.shields.io/pypi/v/cacha?label=PyPI&logo=pypi)](https://pypi.org/project/cacha/)\n[![License](https://img.shields.io/pypi/l/cacha.svg)](https://github.com/smolendawid/cacha/blob/main/LICENSE)\n\nThe simplest Python cache for Data Scientist:\n\n- cache on disk, use between runs,\n- use at function call, not definition.\n\n## Example\n\nIf you don\'t want to wait for a given `compute()` function to complete\neach time you run the script, you can cache it:\n\n```python\nimport cacha\n\nresult = compute(data) # regular usage, slow\n\nresult = cacha.cache(compute, (data, ))  # usage with cache\n\n```\n\nThe cached data is stored in `$HOME/.cacha/`. Each time you run the\nfunction with identical input arguments, the output data will be loaded,\ninstead of being computed.\n\nIt can be easily used with popular data structures like `pandas.DataFrame` or\n`numpy.array`. In case of complicated python objects that can\'t be easily\nhashed, you can use an additional `key` parameter that forces saving the cache\nbased on the `key` value.\n\n```python\nimport cacha\n\nresult = cacha.cache(compute, (data, ), key="compute-v3")\n\n```\n\n## FAQ\n\n**How is it different other caching packages?**\n\nIn contrary to many other tools, _cacha_:\n\n- is used at the function call, not definition. Many packages implement\n  the `@cache` decorator that has to be used before definition of\n  a function that is not easy enough to use.\n- it stores the cache on disk which means you can use cache between runs.\n  This is convenient in data science work.\n\n**How can I clear the cache?**\n\nJust delete the `$HOME/.cacha/` directory. You can also call `cacha.clean()`\nwhich has the same effect.\n\n**Why does it require the `pandas`, `numpy` and other libraries?**\n\nTo properly cache the objects from specific packages, it is necessary\nto have access to the functions they provide in that regard.\n\nThe main goal of cache is not to be lightweight but to provide the best\ndeveloper experience.\n\nHowever most of the required packages are usually\nused in Machine Learning projects anyway.\n',
    'author': 'Dawid Smoleń',
    'author_email': 'smolendawid@gmail.com',
    'maintainer': 'Dawid Smoleń',
    'maintainer_email': 'smolendawid@gmail.com',
    'url': 'https://python-poetry.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
