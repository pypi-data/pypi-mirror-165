# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jqlite', 'jqlite.core']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['jqlite = jqlite.cli:main']}

setup_kwargs = {
    'name': 'jqlite',
    'version': '0.4.1',
    'description': 'An implementation of jq for learning purposes.',
    'long_description': '# jqlite\n\nAn implementation of [jq](https://stedolan.github.io/jq/), the commandline JSON processor, for learning and fun.\n\n## Installation\n\n```shell\n> pip install jqlite\n```\n\n## Examples:\n```sh\n> echo \'{"foo": 0}\' | jqlite\n{\n  "foo": 0\n}\n\n> echo \'{"foo": [1, 2, 3, 4]}\' | jqlite \'[.foo | .[] | select(. % 2 == 0) | . * 2]\'\n[\n  4.0,\n  8.0\n]\n```',
    'author': 'Christian',
    'author_email': 'xian.tuxoid@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/christianzzz/jqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
