# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysecuritytxt']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0']}

entry_points = \
{'console_scripts': ['pysecuritytxt = pysecuritytxt:main']}

setup_kwargs = {
    'name': 'pysecuritytxt',
    'version': '0.1.1',
    'description': 'Python CLI and module for querying security.txt files on domains.',
    'long_description': '# Python client and module for querying .well-known/security.txt files\n\nGive it a domain, it tries to fetch the security.txt file\n\n## Installation\n\n```bash\npip install pysecuritytxt\n```\n\n## Usage\n\n### Command line\n\nYou can use the `pysecuritytxt` command:\n\n```bash\nusage: pysecuritytxt [-h] [-p] url_or_domain\n\nTry to get a security.txt file\n\npositional arguments:\n  url_or_domain  Try to get the file from there.\n\noptions:\n  -h, --help     show this help message and exit\n  -p, --parse    Parse the response, returns dict\n```\n\n### Library\n\nSee [API Reference]()\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Lookyloo/pysecuritytxt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
