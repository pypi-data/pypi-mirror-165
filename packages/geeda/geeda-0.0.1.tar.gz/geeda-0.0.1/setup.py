# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['geeda']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.3,<2.0.0', 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'geeda',
    'version': '0.0.1',
    'description': 'General EDA Framework for Pandas DataFrames',
    'long_description': '# geeda\nGee.D.A: General EDA Framework for Pandas DataFrames\n',
    'author': 'Jason Zhang',
    'author_email': 'jasonjzhang17@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
