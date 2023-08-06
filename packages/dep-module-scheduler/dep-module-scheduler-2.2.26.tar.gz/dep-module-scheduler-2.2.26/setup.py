# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dep_scheduler', 'tests']

package_data = \
{'': ['*']}

modules = \
['pyproject']
install_requires = \
['APScheduler>=3.9.1,<4.0.0', 'dep-spec>=2.2.26,<3.0.0', 'poetry==1.1.15']

setup_kwargs = {
    'name': 'dep-module-scheduler',
    'version': '2.2.26',
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
