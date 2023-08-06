# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extract_from_url']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.0.0', 'libarchive-c>=1.0']

setup_kwargs = {
    'name': 'extract-from-url',
    'version': '0.3.0',
    'description': 'Download and extract files on-the-fly (ZIP files too)',
    'long_description': '.. image:: https://img.shields.io/pypi/v/extract_from_url.svg\n    :target: https://pypi.org/project/extract_from_url/\n\nDescription\n===========\n    \nTake advantage of `libarchive <https://libarchive.org/>`_ to download and extract files without having to store the archive first. Works with ZIP files too!\n\nIt supports `pyfilesystem2 <https://www.pyfilesystem.org/>`_ in order to save the files to cloud services, remote resource, as well as local directories.\n\nDependencies\n============\n\n1. `libarchive-c <https://pypi.org/project/libarchive-c/>`_ which requires ``libarchive-devel`` or ``libarchive-dev`` to be built\n2. `tqdm <https://pypi.org/project/tqdm/>`_ for progress bars (optional)\n\nYou can use `poetry <https://poetry.eustace.io/>`_ or `pip <https://pip.pypa.io/>`_ to install the dependencies.\n\nUsage\n=====\n\nAs standalone program\n---------------------\n\nPlease see ``cli.py --help``\n\nAs library\n----------\n\nAvailable as package on `PyPI <https://pypi.org/project/extract-from-url/>`_.\n',
    'author': 'Francesco Frassinelli',
    'author_email': 'francesco.frassinelli@nina.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/frafra/extract-from-url',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
