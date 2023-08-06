# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kgcl_rdflib', 'kgcl_rdflib.apply', 'kgcl_rdflib.diff']

package_data = \
{'': ['*']}

install_requires = \
['kgcl-schema>=0.3.0,<0.4.0',
 'lark>=1.1.2,<2.0.0',
 'linkml-runtime>=1.1.24,<2.0.0']

entry_points = \
{'console_scripts': ['kgcl-apply = kgcl.kgcl:cli',
                     'kgcl-diff = kgcl.kgcl_diff:cli',
                     'kgcl-parse = kgcl.grammar.parser:cli']}

setup_kwargs = {
    'name': 'kgcl-rdflib',
    'version': '0.3.0',
    'description': 'Schema fro the KGCL project.',
    'long_description': '# kgcl-rdflib\n\nAn engine that applies changes or diffs specified in KGCL to an RDF graph stored using rdflib\n\n## KGCL\n\nKGCL (Knowledge Graph Change Language) is a datamodel and language for representing changes in ontologies and knowledge graphs\n\nThe core KGCL repo is here:\n\n - https://github.com/INCATools/kgcl\n \n This kgcl-rdflib repo applies the KGCL model to rdflib graphs.\n\n',
    'author': 'Christian Kindermann',
    'author_email': 'christian.kindermann@postgrad.manchester.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
