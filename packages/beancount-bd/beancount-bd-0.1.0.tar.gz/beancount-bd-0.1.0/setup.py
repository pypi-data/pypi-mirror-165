# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_bd']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.2,<3.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'beancount-bd',
    'version': '0.1.0',
    'description': 'Beancount order history importer for Bourse Direct brooker',
    'long_description': '# Beancount Bourse Direct Importer\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ArthurFDLR/beancount-bd/beancount-bd?style=for-the-badge)](https://github.com/ArthurFDLR/beancount-bd/actions)\n[![PyPI](https://img.shields.io/pypi/v/beancount-bd?style=for-the-badge)](https://pypi.org/project/beancount-bd/)\n[![PyPI - Version](https://img.shields.io/pypi/pyversions/beancount-bd.svg?style=for-the-badge)](https://pypi.org/project/beancount-bd/)\n[![GitHub](https://img.shields.io/github/license/ArthurFDLR/beancount-bd?style=for-the-badge)](https://github.com/ArthurFDLR/beancount-bd/blob/master/LICENSE.txt)\n[![Linting](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n\n`beancount-bd` provides an order history importer for the brooker [Bourse Direct](http://www.boursedirect.fr) to the [Beancount](http://furius.ca/beancount/) format.\n\n## Installation\n\n```console\n    $ pip install beancount-bd\n```\n\n## Usage\n\nAdd ```BDImporter``` to your [Beancount importers config file](https://beancount.github.io/docs/importing_external_data.html#configuration).\n\n```python\nCONFIG = [\n    BDImporter(\n        account=\'Assets:FR:BD:PEA\',\n        fee_category=\'Expenses:Finances:Commission\',\n        tickers_lut={\n            "AM.E.P.SP500": "PE500",\n            "LY.PEANASD": "PUST",\n            "MSC.EM": "PAEEM",\n            "MSC.EUR": "PCEU",\n        }\n    ),\n]\n```\n\n## Contribution\n\nFeel free to contribute!\n\nPlease make sure you have Python 3.6+ and [`Poetry`](https://poetry.eustace.io/) installed.\n\n1. Git clone the repository - `git clone https://github.com/ArthurFDLR/beancount-bd`\n\n2. Install the packages required for development - `poetry install`\n\n3. That\'s basically it. You should now be able to run lint checks and the test suite - `make lint test`.\n',
    'author': 'Arthur Findelair',
    'author_email': 'arthfind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArthurFDLR/beancount-bd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
