# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jdv_funcutils', 'jdv_funcutils.signature', 'jdv_funcutils.utils']

package_data = \
{'': ['*']}

extras_require = \
{'documentation': ['Sphinx>=5.0.1,<6.0.0',
                   'sphinx-rtd-theme>=1.0.0,<2.0.0',
                   'sphinx-autodoc-typehints>=1.18.2,<2.0.0',
                   'PyYAML>=6.0,<7.0']}

setup_kwargs = {
    'name': 'jdv-funcutils',
    'version': '1.0.1',
    'description': 'Function utilties.',
    'long_description': None,
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@justbiotherapeutics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
