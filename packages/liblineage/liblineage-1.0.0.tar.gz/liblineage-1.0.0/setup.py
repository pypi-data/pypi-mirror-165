# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liblineage',
 'liblineage.constants',
 'liblineage.hudson',
 'liblineage.ota',
 'liblineage.wiki',
 'liblineage.wiki.data_types']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'sebaubuntu-libs>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'liblineage',
    'version': '1.0.0',
    'description': 'LineageOS utils library',
    'long_description': '# liblineage\n\n[![PyPi version](https://img.shields.io/pypi/v/liblineage)](https://pypi.org/project/liblineage/)\n\nLineageOS utils library\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install liblineage\n```\n\n## Instructions\n\n```sh\npython3 -m liblineage\n```\n\n## License\n\n```\n#\n# Copyright (C) 2022 The LineageOS Project\n#\n# SPDX-License-Identifier: LGPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sebaubuntu-python/liblineage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
