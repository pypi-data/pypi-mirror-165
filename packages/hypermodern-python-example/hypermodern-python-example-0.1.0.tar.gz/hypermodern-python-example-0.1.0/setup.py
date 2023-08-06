# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_example']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'importlib-metadata>=4.12.0,<5.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-example = '
                     'hypermodern_python_example.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-example',
    'version': '0.1.0',
    'description': 'The hypermodern Python example',
    'long_description': '[![Tests](https://github.com/paulrousset/hypermodern-python-example/workflows/Tests/badge.svg)](https://github.com/paulrousset/hypermodern-python-example/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/paulrousset/hypermodern-python-example/branch/master/graph/badge.svg)](https://codecov.io/gh/paulrousset/hypermodern-python-example)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-example.svg)](https://pypi.org/project/hypermodern-python-example/)\n[![Read the Docs](https://readthedocs.org/projects/hypermodern-python-example/badge/)](https://hypermodern-python-example.readthedocs.io/)\n\n# hypermodern-python-example\nExample of setup with hypermodern python tooling\n\n',
    'author': 'Paul',
    'author_email': 'paulrousset@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/username/hypermodern-python-example',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
