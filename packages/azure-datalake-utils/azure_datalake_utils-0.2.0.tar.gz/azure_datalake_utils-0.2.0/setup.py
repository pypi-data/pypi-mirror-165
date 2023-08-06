# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azure_datalake_utils', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['adlfs<=2022.7.0',
 'azure-identity>=1.10.0,<2.0.0',
 'click>=8.0.2,<9.0.0',
 'fsspec<=2021.10.1',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.0,<2.0.0']

extras_require = \
{':extra == "test"': ['ipykernel>=6.15.2,<7.0.0', 'Jinja2>=2.11.1,<3.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=22.0,<23.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.3,<2.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=8.0,<9.0',
         'mkdocstrings[python]>=0.19.0,<0.20.0',
         'mkdocs-autorefs>=0.3,<0.4'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0',
          'markupsafe==2.0.1']}

setup_kwargs = {
    'name': 'azure-datalake-utils',
    'version': '0.2.0',
    'description': 'Utilidades para interactuar con Azure Datalake.',
    'long_description': '# Azure Datalake Utils\n\n\n[![pypi](https://img.shields.io/pypi/v/azure-datalake-utils.svg)](https://pypi.org/project/azure-datalake-utils/)\n[![python](https://img.shields.io/pypi/pyversions/azure-datalake-utils.svg)](https://pypi.org/project/azure-datalake-utils/)\n[![Build Status](https://github.com/centraal-api/azure-datalake-utils/actions/workflows/dev.yml/badge.svg)](https://github.com/centraal-api/azure-datalake-utils/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/centraal-api/azure-datalake-utils/branch/main/graphs/badge.svg)](https://codecov.io/github/centraal-api/azure-datalake-utils)\n\n\n\nUtilidades para interactuar con Azure Datalake.\n\nEl objetivo es evitar que personas denominadas cientificos ciuidanos tengan que interactuar con librerias, que no son, totalmente relacionadas con el analisis de datos.\n\nLa hipotesis detras de este pensamiento es que se puede lograr incrementar la adopción de estas herramientas si se facilitan y simplifica la interacción de pandas con la lectura del datalake.\n\n* Documentation: <https://centraal-api.github.io/azure-datalake-utils>\n* GitHub: <https://github.com/centraal-api/azure-datalake-utils>\n* PyPI: <https://pypi.org/project/azure-datalake-utils/>\n* Free software: Apache-2.0\n\n\n## Features\n\n* Control de autenticación directamente con el Directorio activo de Azure.\n* Lectura de archivos csv y excel, de una forma más concisa.\n\n## Credits\n\nLa librería es creada y mantenida por [Centraal Studio](https://centraal.studio/).\n \nCentraal Studio Agredece la alianza con [Haceb](https://www.haceb.com/), cuyos retos internos  de democratizar el acceso a información han motivado la creación de esta librería.\n\n//\n\nThis package is created and mantained by [Centraal Studio](https://centraal.studio/).\n\nCentraal Studio appreciate the alliance with [Haceb](https://www.haceb.com/), which internal efforts to democratize the access of company information has motivated the creation of the library.\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'centraal.studio',
    'author_email': 'equipo@centraal.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/centraal-api/azure-datalake-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
