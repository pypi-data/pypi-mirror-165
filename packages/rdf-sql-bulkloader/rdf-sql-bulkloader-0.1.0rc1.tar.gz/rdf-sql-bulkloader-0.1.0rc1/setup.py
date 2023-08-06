# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rdf_sql_bulkloader', 'rdf_sql_bulkloader.loaders']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'curies>=0.2.0,<0.3.0',
 'importlib>=1.0.4,<2.0.0',
 'lightrdf>=0.2.1,<0.3.0',
 'prefixmaps>=0.1.2,<0.2.0',
 'setuptools>=64.0.1,<65.0.0',
 'tox>=3.25.1,<4.0.0']

entry_points = \
{'console_scripts': ['rdf-sql-bulkloader = rdf_sql_bulkloader.cli:main']}

setup_kwargs = {
    'name': 'rdf-sql-bulkloader',
    'version': '0.1.0rc1',
    'description': 'rdf-sql-bulkloader',
    'long_description': None,
    'author': 'Chris Mungall',
    'author_email': 'cjmungall@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
