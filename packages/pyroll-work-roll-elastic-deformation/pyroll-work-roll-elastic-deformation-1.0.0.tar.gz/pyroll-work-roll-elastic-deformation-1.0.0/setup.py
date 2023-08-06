# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['work_roll_elastic_deformation']

package_data = \
{'': ['*']}

install_requires = \
['cad-to-shapely>=0.3.0,<0.4.0', 'pyroll-basic>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-work-roll-elastic-deformation',
    'version': '1.0.0',
    'description': 'Plugin for PyRoll calculating the bending of the work roll by matrix method',
    'long_description': '# PyRoll Work Roll Elastic Deformation\n\nPlugin for PyRolL providing the calculation of elastic work roll deformation by matrix method.\n\nFor the docs, see [here](docs/docs.pdf).\n\nThis project is licensed under the [BSD-3-Clause license](LICENSE).\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-work-roll-elastic-deformation/) and can be installed with\n    \n    pip install pyroll-work-roll-elastic-deformation',
    'author': 'Christoph Renzing',
    'author_email': 'christoph.renzing@imf.tu-freiberg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
