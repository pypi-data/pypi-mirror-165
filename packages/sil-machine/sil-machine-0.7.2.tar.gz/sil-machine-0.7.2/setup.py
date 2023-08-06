# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine',
 'machine.annotations',
 'machine.clusterers',
 'machine.corpora',
 'machine.scripture',
 'machine.tokenization',
 'machine.tokenization.sentencepiece',
 'machine.translation',
 'machine.translation.tensorflow',
 'machine.translation.thot',
 'machine.utils',
 'machine.webapi']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=4.0.0,<5.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.19.0,<2.0.0',
 'regex>=2021.7.6,<2022.0.0',
 'sortedcontainers>=2.4.0,<3.0.0']

extras_require = \
{':extra == "sentencepiece" or extra == "all"': ['sentencepiece>=0.1.95,<0.2.0'],
 ':extra == "tensorflow" or extra == "all"': ['libclang>=11.1.0,<12.0.0',
                                              'tensorflow>=2.7.0,<3.0.0',
                                              'OpenNMT-tf>=2.25.0,<3.0.0'],
 ':extra == "thot" or extra == "all"': ['sil-thot>=3.3.6,<4.0.0'],
 ':extra == "webapi" or extra == "all"': ['clearml>=1.4.1,<2.0.0',
                                          'json-stream>=1.3.0,<2.0.0'],
 ':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=4.2.0,<5.0.0']}

setup_kwargs = {
    'name': 'sil-machine',
    'version': '0.7.2',
    'description': 'A natural language processing library that is focused on providing tools for resource-poor languages.',
    'long_description': '# Machine for Python\n\nMachine is a natural language processing library. It is specifically focused on providing tools and techniques that are useful for processing languages that are very resource-poor. The library is also useful as a foundation for building more advanced language processing techniques. The library currently only provides a basic set of algorithms, but the goal is to include many more in the future.\n\n## Installation\n\nMachine is available as a pip package:\n\n```\npip install sil-machine\n```\n\n## Tutorials\n\nIf you would like to find out more about how to use Machine, check out the tutorial Jupyter notebooks:\n\n- [Tokenization](samples/tokenization.ipynb)\n- [Text Corpora](samples/corpora.ipynb)\n- [Word Alignment](samples/word_alignment.ipynb)\n',
    'author': 'SIL International',
    'author_email': 'None',
    'maintainer': 'Damien Daspit',
    'maintainer_email': 'damien_daspit@sil.org',
    'url': 'https://github.com/sillsdev/machine.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
