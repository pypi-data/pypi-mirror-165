# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'cursed_hr': 'src/cursed_hr',
 'hr': 'src/hr',
 'opennetzteil': 'src/opennetzteil',
 'penlog': 'src/penlog'}

packages = \
['cursed_hr',
 'gallia',
 'gallia.commands',
 'gallia.commands.discover',
 'gallia.commands.discover.uds',
 'gallia.commands.fuzz',
 'gallia.commands.fuzz.uds',
 'gallia.commands.primitive',
 'gallia.commands.primitive.uds',
 'gallia.commands.scan',
 'gallia.commands.scan.uds',
 'gallia.commands.script',
 'gallia.db',
 'gallia.services',
 'gallia.services.xcp',
 'gallia.transports',
 'gallia.uds',
 'gallia.uds.core',
 'gallia.udscan',
 'hr',
 'opennetzteil',
 'penlog']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'argcomplete>=2.0.0,<3.0.0',
 'construct>=2.10.68,<3.0.0',
 'msgspec>=0.8.0,<0.9.0',
 'python-can>=4.0.0,<5.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tomlkit>=0.11.0,<0.12.0',
 'xdg>=5.1.1,<6.0.0',
 'zstandard>=0.17,<0.19']

entry_points = \
{'console_scripts': ['cursed-hr = cursed_hr.cursed_hr:main',
                     'discover-xcp = gallia.udscan.scanner.find_xcp:main',
                     'gallia = gallia.cli:main',
                     'hr = hr:main']}

setup_kwargs = {
    'name': 'gallia',
    'version': '1.1.0a1',
    'description': 'Extendable Pentesting Framework',
    'long_description': '<!--\nSPDX-FileCopyrightText: AISEC Pentesting Team\n\nSPDX-License-Identifier: CC0-1.0\n-->\n\n# Gallia\n\n[![docs](https://img.shields.io/badge/-docs-green)](https://fraunhofer-aisec.github.io/gallia)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gallia)](https://pypi.python.org/pypi/gallia/)\n[![PyPI - License](https://img.shields.io/pypi/l/gallia)](https://www.apache.org/licenses/LICENSE-2.0.html)\n[![PyPI](https://img.shields.io/pypi/v/gallia)](https://pypi.python.org/pypi/gallia/)\n\nGallia is an extendable pentesting framework with the focus on the automotive domain.\nThe scope of the toolchain is conducting penetration tests from a single ECU up to whole cars.\nCurrently, the main focus lies on the [UDS](https://www.iso.org/standard/72439.html) interface.\nTaking advantage of this modular design, the [logging and archiving](https://fraunhofer-aisec.github.io/gallia/penlog.7.html) functionality was developed separately.\nActing as a generic interface, the logging functionality implements reproducible tests and enables post-processing tasks.\nThe [rendered documentation](https://fraunhofer-aisec.github.io/gallia) is available via Github Pages.\n\nKeep in mind that this project is intended for research and development usage only!\nInappropriate usage might cause irreversible damage to the device under test.\nWe do not take any responsibility for damage caused by the usage of this tool.\n\n## Quickstart\n\nSee the [setup instructions](https://fraunhofer-aisec.github.io/gallia/setup.html).\n\n```\n$ gallia primitive uds dtc --target "isotp://can0?src_addr=0x123&dst_addr=0x312&tx_padding=0xaa&rx_padding=0xaa" read\n```\n\nFor specifying the `--target` argument see the [transports documentation](https://fraunhofer-aisec.github.io/gallia/transports.html).\n\n## Acknowledgments\n\nThis work was partly funded by the German Federal Ministry of Education and Research (BMBF) as part of the [SecForCARs](https://www.secforcars.de/) project (grant no. 16KIS0790).\nA short presentation and demo video is available at this [page](https://www.secforcars.de/demos/10-automotive-scanning-framework.html).\n',
    'author': 'AISEC Pentesting Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Fraunhofer-AISEC/gallia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
