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
    'version': '0.1.1',
    'description': 'rdf-sql-bulkloader',
    'long_description': '# rdf-sql-bulkloader\n\nBulk load of SQL table from RDF in Python\n\n## Install\n\n```bash\npip install rdf-sql-bulkloader\n```\n\n## Usage (Command Line)\n\n```\nrdf-sql-bulkloader load-sqlite  -o cl.db cl.owl\n```\n\nNote: currently only sqlite supported\n\n## Usage (Programmatic)\n\nSee tests\n\n## Core table\n\n```\nCREATE TABLE statement (\n\tid TEXT,\n\tsubject TEXT,\n\tpredicate TEXT,\n\tobject TEXT,\n\tvalue TEXT,\n\tdatatype TEXT,\n\tlanguage TEXT,\n        graph TEXT\n);\n```\n\n## Prefixes\n\nthis uses the merged prefixmap from [prefixmaps](https://github.com/linkml/prefixmaps) by default\n\nThis can be overridden programmatically when instantiating a loader, e.g\n\nExplicit map:\n\n```python\nloader = SqliteBulkloader(path=path, prefix_map={...})\n```\n\nUsing pre-registered:\n\n```python\nloader = SqliteBulkloader(path=path, named_prefix_maps=["obo", "prefixcc"])\n```\n\n- TODO: add override from CLI\n\n\n## Acknowledgements\n\nThis work was entirely inspired by James Overton\'s [rdftab.rs](https://github.com/ontodev/rdftab.rs\n\nThis [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) project was developed from the [sphintoxetry-cookiecutter](https://github.com/hrshdhgd/sphintoxetry-cookiecutter) template and will be kept up-to-date using [cruft](https://cruft.github.io/cruft/).\n',
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
