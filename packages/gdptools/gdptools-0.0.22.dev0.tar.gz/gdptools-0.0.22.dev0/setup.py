# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_pygeoapi_process', 'gdptools', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*', 'data/TM_WORLD_BORDERS_SIMPL-0.3/*']}

install_requires = \
['MetPy>=1.3.0,<2.0.0',
 'Pydap>=3.2.2,<4.0.0',
 'Shapely>=1.8.4,<2.0.0',
 'attr>=0.3.2,<0.4.0',
 'attrs>=21.4.0,<22.0.0',
 'cftime>=1.6.0,<2.0.0',
 'click<8',
 'dask>=2022.6.0,<2023.0.0',
 'geopandas>=0.11.1,<0.12.0',
 'intake>=0.6.5,<0.7.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'pygeoapi>=0.11.0,<0.12.0',
 'pygeos>=0.13.0,<0.14.0',
 'pyproj>=3.3.1,<4.0.0',
 'pystac>=1.4.0,<2.0.0',
 'rasterio>=1.2.10,<2.0.0',
 'rasterstats>=0.16.0,<0.17.0',
 'requests>=2.28.0,<3.0.0',
 'rioxarray>=0.11.1,<0.12.0',
 'scipy>=1.8.1,<2.0.0',
 'xarray>=2022.3.0,<2023.0.0',
 'zarr>=2.11.3,<3.0.0']

entry_points = \
{'console_scripts': ['gdptools = gdptools.__main__:main']}

setup_kwargs = {
    'name': 'gdptools',
    'version': '0.0.22.dev0',
    'description': 'Gdptools',
    'long_description': "# Readme\n\n[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![Latest Release](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/badges/release.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/releases)\n[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)\n[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)\n[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)\n[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Gdptools_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n        pip install gdptools\n\n## Usage\n\nPlease see the [Command-line Reference](Usage_) for details.\n\n## Contributing\n\nContributions are very welcome. To learn more, see the Contributor Guide\\_.\n\n## License\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), _Gdptools_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/issues) along with a detailed description.\n\n## Credits\n\nThis project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.\n",
    'author': 'Richard McDonald',
    'author_email': 'rmcd@usgs.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/gdptools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
