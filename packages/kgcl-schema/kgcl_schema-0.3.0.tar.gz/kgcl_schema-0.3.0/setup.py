# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kgcl_schema',
 'kgcl_schema.datamodel',
 'kgcl_schema.grammar',
 'kgcl_schema.schema']

package_data = \
{'': ['*']}

install_requires = \
['bioregistry>=0.5.49,<0.6.0',
 'lark>=1.1.2,<2.0.0',
 'linkml-runtime>=1.1.24,<2.0.0']

entry_points = \
{'console_scripts': ['kgcl-apply = kgcl_schema.kgcl:cli',
                     'kgcl-diff = kgcl_schema.kgcl_diff:cli',
                     'kgcl-parse = kgcl_schema.grammar.parser:cli']}

setup_kwargs = {
    'name': 'kgcl-schema',
    'version': '0.3.0',
    'description': 'Schema for the KGCL project.',
    'long_description': '# KGCL: Knowledge Graph Change Language\n\nKGCL is a standard datamodel for representing changes in ontologies and knowledge graphs.\n\nThis repository houses:\n\n- The KGCL schema/standard\n- The Python implementation of the standard (LinkML model, LARK grammar)\n\n## Documentation\n\n[Read more here.](https://incatools.github.io/kgcl/)\n\n',
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
