# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ensembleperturbation',
 'ensembleperturbation.client',
 'ensembleperturbation.parsing',
 'ensembleperturbation.perturbation',
 'ensembleperturbation.plotting',
 'ensembleperturbation.uncertainty_quantification']

package_data = \
{'': ['*']}

install_requires = \
['adcircpy>=1.1.0',
 'appdirs',
 'beautifulsoup4',
 'chaospy',
 'coupledmodeldriver>=1.5',
 'dask',
 'f90nml',
 'fiona',
 'geopandas',
 'netcdf4',
 'numpy',
 'pandas',
 'pint-pandas',
 'pyproj>=2.6',
 'python-dateutil',
 'requests',
 'scikit-learn',
 'shapely',
 'stormevents>=1.4.1',
 'tables',
 'typepigeon']

extras_require = \
{'development': ['isort', 'oitnb'],
 'documentation': ['m2r2',
                   'sphinx',
                   'sphinx-rtd-theme',
                   'sphinxcontrib-bibtex',
                   'sphinxcontrib-programoutput'],
 'plotting': ['cartopy', 'cmocean', 'matplotlib'],
 'testing': ['pytest', 'pytest-cov', 'pytest-xdist', 'wget']}

entry_points = \
{'console_scripts': ['combine_results = '
                     'ensembleperturbation.client.combine_results:main',
                     'make_storm_ensemble = '
                     'ensembleperturbation.client.make_storm_ensemble:main',
                     'perturb_tracks = '
                     'ensembleperturbation.client.perturb_tracks:main',
                     'plot_results = '
                     'ensembleperturbation.client.plot_results:main']}

setup_kwargs = {
    'name': 'ensembleperturbation',
    'version': '1.1.0',
    'description': 'perturbation of coupled model input over a space of input variables',
    'long_description': '# Ensemble Perturbation\n\n[![tests](https://github.com/noaa-ocs-modeling/EnsemblePerturbation/workflows/tests/badge.svg)](https://github.com/noaa-ocs-modeling/EnsemblePerturbation/actions?query=workflow%3Atests)\n[![codecov](https://codecov.io/gh/noaa-ocs-modeling/ensembleperturbation/branch/main/graph/badge.svg?token=4DwZePHp18)](https://codecov.io/gh/noaa-ocs-modeling/ensembleperturbation)\n[![build](https://github.com/noaa-ocs-modeling/EnsemblePerturbation/workflows/build/badge.svg)](https://github.com/noaa-ocs-modeling/EnsemblePerturbation/actions?query=workflow%3Abuild)\n[![version](https://img.shields.io/pypi/v/EnsemblePerturbation)](https://pypi.org/project/EnsemblePerturbation)\n[![license](https://img.shields.io/github/license/noaa-ocs-modeling/EnsemblePerturbation)](https://creativecommons.org/share-your-work/public-domain/cc0)\n[![style](https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw)](https://sourceforge.net/p/oitnb/code)\n[![documentation](https://readthedocs.org/projects/ensembleperturbation/badge/?version=latest)](https://ensembleperturbation.readthedocs.io/en/latest/?badge=latest)\n\nPython library for perturbing coupled model inputs into ensemble runs. Provides\nperturbation and results comparison.\n\n```bash\npip install ensembleperturbation\n```\n\nDocumentation can be found at https://ensembleperturbation.readthedocs.io\n\n## Command-line interface\n\n`ensembleperturbation` exposes the following CLI commands:\n\n- `make_storm_ensemble`\n- `perturb_tracks`\n- `combine_results`\n- `plot_results`\n',
    'author': 'Zach Burnett',
    'author_email': 'zachary.burnett@noaa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noaa-ocs-modeling/EnsemblePerturbation.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
