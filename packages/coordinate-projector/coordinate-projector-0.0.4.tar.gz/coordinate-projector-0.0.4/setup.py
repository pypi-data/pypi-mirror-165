# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coordinate_projector']

package_data = \
{'': ['*']}

install_requires = \
['pyproj>=3.3.0,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'timezonefinder',
 'types-python-dateutil>=2.8.9,<3.0.0']

setup_kwargs = {
    'name': 'coordinate-projector',
    'version': '0.0.4',
    'description': 'Project points from one projection to another using pyproj',
    'long_description': '# Coordinate Projector\n\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\nThis is the Norwegian Geotechnical Institute (NGI) Python package for projecting coordinates. \nIt is a small shim on top of the library [pyproj](https://github.com/pyproj4/pyproj) that again is an interface to \n [PROJ](https://proj.org/).  \n\nReferences:\n\nLatest releases see [CHANGES.md](CHANGES.md)\n\n# Installation (end user) \n\n```bash\n\npip install coordinate-projector\n\n```\n\n## Basic usage\n\n### Project a point\n\n```python\nfrom coordinate_projector import Projector\n\nprojector = Projector()\n \nfrom_srid = "4326"\nto_srid = "3857"\n\n# Paris Lat(48.8589506) Lon(2.2768485) EPSG:4326\nfrom_east, from_north = 2.2768485, 48.8589506 \n\nprojected_east, projected_north = projector.transform(from_srid, to_srid, from_east, from_north)\n\n# Paris Lat(6250962.06) Lon(253457.62) EPSG:3857 is in metres - 2D projection\nassert abs(projected_east - 253457.62) <= 0.01\nassert abs(projected_north - 6250962.06) <= 0.01 \n\nprint(f"{projected_east=}, {projected_north=}")\n# projected_east=253457.6156334287, projected_north=6250962.062720417\n```\n\n# Getting Started developing\n\n1. Software dependencies\n\n   - Python 3.9 or higher\n   - Poetry\n   - black code formatter\n\n2. Clone this repository\n\n3. Install\n\n   `poetry install`\n\n\n\n# Build and Test\n\nRun in the project root folder: \n\n    poetry shell pytest \n\nBuild the package wheel: \n\n    poetry build\n\n# Publish\n\n# TODOs\n\n- Handle lines\n- Handle polygons\n\n# Contribute\n\nPlease start by adding an issue before submitting any pull requests.\n\n',
    'author': 'Helge Smebye',
    'author_email': None,
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
