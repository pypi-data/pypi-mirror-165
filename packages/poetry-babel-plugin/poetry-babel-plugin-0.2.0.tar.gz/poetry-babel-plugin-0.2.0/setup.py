# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_babel_plugin']

package_data = \
{'': ['*']}

install_requires = \
['babel>=2.10.1,<3.0.0', 'poetry>=1.2.0,<1.3.0']

entry_points = \
{'poetry.application.plugin': ['babel = '
                               'poetry_babel_plugin.plugin:BabelPlugin']}

setup_kwargs = {
    'name': 'poetry-babel-plugin',
    'version': '0.2.0',
    'description': 'Babel plugin for poetry',
    'long_description': 'None',
    'author': 'Stepan Henek',
    'author_email': 'stepan@henek.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
