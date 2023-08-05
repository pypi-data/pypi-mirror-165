# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dep_scheduler', 'tests']

package_data = \
{'': ['*']}

modules = \
['pyproject']
install_requires = \
['APScheduler>=3.9.1,<4.0.0', 'dep-spec>=1.2.13,<2.0.0']

setup_kwargs = {
    'name': 'dep-module-scheduler',
    'version': '1.2.13',
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
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
