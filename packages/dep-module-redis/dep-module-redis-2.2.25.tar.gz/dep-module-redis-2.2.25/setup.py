# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dep_redis', 'tests']

package_data = \
{'': ['*']}

modules = \
['pyproject']
install_requires = \
['aioredis[hiredis]>=2.0.1,<3.0.0', 'dep-spec>=2.2.25,<3.0.0', 'poetry==1.1.15']

setup_kwargs = {
    'name': 'dep-module-redis',
    'version': '2.2.25',
    'description': '',
    'long_description': None,
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<=3.9.13',
}


setup(**setup_kwargs)
