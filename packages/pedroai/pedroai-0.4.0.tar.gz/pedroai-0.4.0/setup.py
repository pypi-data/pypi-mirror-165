# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pedroai']

package_data = \
{'': ['*']}

install_requires = \
['altair-saver>=0.5.0,<0.6.0',
 'altair>=4.2.0,<5.0.0',
 'plotnine>=0.9,<0.10',
 'pydantic>=1.9.0,<2.0.0',
 'pysimdjson[dev]>=4.0.3,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.1,<13.0.0',
 'scipy>=1.7.3,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pedroai = pedroai.main:cli']}

setup_kwargs = {
    'name': 'pedroai',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Pedro Rodriguez',
    'author_email': 'me@pedro.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
