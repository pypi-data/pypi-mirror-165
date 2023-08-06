# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyjuliacall', 'tyjuliasetup']

package_data = \
{'': ['*']}

install_requires = \
['julia>=0.5.7,<0.6.0', 'wisepy2>=1.3,<2.0']

entry_points = \
{'console_scripts': ['mk-ty-sysimage = tyjuliasetup.cli:mkimage']}

setup_kwargs = {
    'name': 'tyjuliacall',
    'version': '0.1.0',
    'description': 'Tongyuan-hacked PyJulia+JuliaCall (PythonCall+PyCall) integration as an engineerization for Python-Julia interops.',
    'long_description': None,
    'author': 'Suzhou-Tongyuan',
    'author_email': 'support@tongyuan.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
