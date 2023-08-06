# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gasify']

package_data = \
{'': ['*']}

install_requires = \
['plenary>=1.4.3,<2.0.0', 'uncertainties>=3.1.7,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['Pint==0.18'],
 ':python_version >= "3.8"': ['Pint>=0.19.2,<0.20.0']}

setup_kwargs = {
    'name': 'gasify',
    'version': '1.2.2',
    'description': 'A module for handling data from experiments, primarily focused upon gas measurement',
    'long_description': "# gasify\n\n![license](https://img.shields.io/github/license/swinburne-sensing/gasify) ![python version](https://img.shields.io/pypi/pyversions/gasify) ![testing](https://github.com/swinburne-sensing/gasify/actions/workflows/python.yml/badge.svg) ![issues](https://img.shields.io/github/issues/swinburne-sensing/gasify)\n\nA library for handling data from experiments, primarily focused upon gas sensing results. Contains methods for calculation of humidity, gas concentrations, gas mixtures, gas correction factors, and handling of various engineering and scientific units (extended from [pint](https://pint.readthedocs.io/en/stable/)).\n\nFormally known as `experimentutil` (un-released).\n\n## Acknowledgments\n\nDeveloped at [Swinburne University of Technology](https://swin.edu.au).\n\n*This activity received funding from [ARENA](https://arena.gov.au) as part of ARENA’s Research and Development Program – Renewable Hydrogen for Export (Contract No. 2018/RND012). The views expressed herein are not necessarily the views of the Australian Government, and the Australian Government does not accept responsibility for any information or advice contained herein.*\n\n*The work has been supported by the [Future Energy Exports CRC](https://www.fenex.org.au) whose activities are funded by the Australian Government's Cooperative Research Centre Program.*\n",
    'author': 'Chris Harrison',
    'author_email': '629204+ravngr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
