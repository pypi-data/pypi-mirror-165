# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kof_parser']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1.7,<3.0.0',
 'coordinate-projector>=0.0.4,<0.0.5',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'kof-parser',
    'version': '0.0.8',
    'description': "A KOF file parser. Follows Norkart's KOF 2.0 specification from 2005.",
    'long_description': "# NGI KOF Parser\n\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![security: safety](https://img.shields.io/badge/security-safety-yellow.svg)](https://github.com/pyupio/safety)\n[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)\n\n\n\nPython package for parsing KOF files.\n\nReferences:\n\nNORWEGIAN GEOTECHNICAL SOCIETY\n- [NGF - VEILEDNING FOR\nSYMBOLER OG DEFINISJONER I GEOTEKNIKK](http://ngf.no/wp-content/uploads/2015/03/2_NGF-ny-melding-2-endelig-utgave-2011-12-04-med-topp-og-bunntekst-Alt-3.pdf)\n- [Norkart KOF specification](http://www.anleggsdata.no/wp-content/uploads/2018/04/KOF-BESKRIVELSE-Oppdatert2005.pdf)\n\nLatest releases see [CHANGES.md](https://github.com/norwegian-geotechnical-institute/kof-parser/blob/main/CHANGES.md)\n\n# Installation (end user) \n\n```bash\n\npip install kof-parser\n\n```\n\n## Basic usage\n\n### Read a kof file\n\n```python\nfrom kof_parser import KOFParser\n\nparser = KOFParser()\n\n# ETRS89/NTM10:\nsrid = 5110\n\nlocations = parser.parse('tests/data/test.kof', result_srid=srid, file_srid=srid)\n\nfor location in locations:\n    print(location)\n\n# Output:\n# name='SMPLOC1' methods=[] point_easting=112892.81 point_northing=1217083.64 point_z=1.0 srid=5110\n# name='SMPLOC2' methods=['TOT'] point_easting=112893.15 point_northing=1217079.46 point_z=2.0 srid=5110\n# name='SMPLOC3' methods=['CPT'] point_easting=112891.88 point_northing=1217073.01 point_z=0.0 srid=5110\n# name='SMPLOC4' methods=['RP'] point_easting=112891.9 point_northing=1217067.54 point_z=0.0 srid=5110\n# name='SMPLOC5' methods=['SA'] point_easting=112902.92 point_northing=1217074.73 point_z=0.0 srid=5110\n# name='SMPLOC6' methods=['PZ'] point_easting=112901.11 point_northing=1217069.56 point_z=0.0 srid=5110\n# name='SMPLOC7' methods=['PZ'] point_easting=1217069.56 point_northing=112901.11 point_z=0.0 srid=5110\n\n```\n\n### Write a kof file\n\n```python\nfrom kof_parser import KOFWriter\nfrom kof_parser import Location\n\nkof_writer = KOFWriter()\n\nsrid = 5110\nlocations = [Location(name='SMPLOC1', point_easting=112892.81, point_northing=1217083.64, point_z=1.0),\n             Location(name='SMPLOC2', point_easting=112893.15, point_northing=1217079.46, point_z=2.0, methods=['TOT']),\n             Location(name='SMPLOC3', point_easting=112891.88, point_northing=1217073.01, point_z=0.0, methods=['CPT'])]\n\nkof_string = kof_writer.writeKOF(\n    project_id='project_id', project_name='cool-name', locations=locations, srid=srid\n)\n\nprint(kof_string)\n# Output:\n# 00 KOF Export from NGI's KOF parser\n# 00 Project: project_id. Name: cool-name\n# 00 Spatial Reference ID (SRID): 5110\n# 00 Export date (UTC): 2022-08-22 13:49:44.394607\n# 00 Oppdrag      Dato     Ver K.sys   Komm $21100000000 Observer    \n# 01 cool-name    22082022   1     210      $11100000000             \n# 05 SMPLOC1             1217083.640  112892.810  1.000                \n# 05 SMPLOC2    2418     1217079.460  112893.150  2.000                \n# 05 SMPLOC3    2407     1217073.010  112891.880  0.000                \n```\n\n# Getting Started developing\n\n1. Software dependencies\n\n2. Clone this repository\n\n3. Install\n\n## Software dependencies\n\nBefore you start, install:\n\n   - Python 3.9 or higher\n   - Poetry\n   - black code formatter\n   \n## Clone this repository\n\nUse git to clone this repository.\n\n## Install\n\nThere are several combinations of how to set up a local development environment.\n\nWe use Poetry for dependency management. See [Install poetry](https://python-poetry.org/docs/) if needed.\n\nThen, from the project root folder run:\n\n    poetry install\n\n\n# Build and Test\n\nRun in the project root folder: \n\n    poetry install\n    poetry run pytest \n\nBuild the package wheel: \n\n    poetry build\n\n# Contribute\n\nPlease start by adding an issue before submitting any pull requests.",
    'author': 'Jostein Leira',
    'author_email': 'jostein@leira.net',
    'maintainer': 'Jostein Leira',
    'maintainer_email': 'jostein@leira.net',
    'url': 'https://ngi.no',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
