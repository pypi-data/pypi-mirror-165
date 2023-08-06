# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roxieapi', 'roxieapi.cadata', 'roxieapi.input_builder']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.9.0,<6.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pymbse-commons>=0.0.6,<0.0.7',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'roxie-api',
    'version': '0.0.11',
    'description': 'A Python API for ROXIE to build a model data input, modify cable database file, and control simulation with a tool adapter',
    'long_description': '# ROXIE API\n\nThis is a project for extraction of ROXIE API from MagNum API for code sharing with the ROXIE team.',
    'author': 'mmaciejewski',
    'author_email': 'michal.maciejewski@ief.ee.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.cern.ch/roxie/roxie-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
