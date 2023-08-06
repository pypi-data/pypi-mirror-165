# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hm_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.17.1,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-click>=7.1.8,<8.0.0']

entry_points = \
{'console_scripts': ['hm-python = hm_python.console:main']}

setup_kwargs = {
    'name': 'hm-python',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '[![Tests](https://github.com/carlpayne/hm-python/workflows/Tests/badge.svg)](https://github.com/carlpayne/hm-python/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/carlpayne/hm-python/branch/master/graph/badge.svg)](https://codecov.io/gh/carlpayne/hm-python)\n[![PyPI](https://img.shields.io/pypi/v/hm-python.svg)](https://pypi.org/project/hm-python/)\n# hm-python\n',
    'author': 'Carl Payne',
    'author_email': 'cpayne@lightricks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/carlpayne/hm-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
