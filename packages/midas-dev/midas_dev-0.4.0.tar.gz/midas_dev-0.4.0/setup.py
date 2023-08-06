# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['midas_dev']

package_data = \
{'': ['*']}

install_requires = \
['Flake8-pyproject>=0.9.0,<0.10.0',
 'asynctest>=0.13.0,<0.14.0',
 'black>=22.6.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'flake8-broken-line>=0.5.0,<0.6.0',
 'flake8-debugger>=4.1.2,<5.0.0',
 'flake8-mock>=0.3,<0.4',
 'flake8-print>=5.0.0,<6.0.0',
 'flake8-pytest-style>=1.6.0,<2.0.0',
 'flake8-use-fstring>=1.4,<2.0',
 'flake8>=4.0.1,<5.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.971,<0.972',
 'poetry>=1.1.15,<2.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'pytest-blockage>=0.2.4,<0.3.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-deadfixtures>=2.2.1,<3.0.0',
 'pytest-env>=0.6.2,<0.7.0',
 'pytest-timeout>=2.1.0,<3.0.0',
 'pytest>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['midblack = midas_dev.main:run_black',
                     'midfmt = midas_dev.main:run_fmt',
                     'midisort = midas_dev.main:run_isort',
                     'midlint = midas_dev.main:run_lint',
                     'midmypy = midas_dev.main:run_mypy',
                     'midpytest = midas_dev.main:run_pytest',
                     'midtest = midas_dev.main:run_test']}

setup_kwargs = {
    'name': 'midas-dev',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Anton V',
    'author_email': 'anton.vasilyev@midas.investments',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
