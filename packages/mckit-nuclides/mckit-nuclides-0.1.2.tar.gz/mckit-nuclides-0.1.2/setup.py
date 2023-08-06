# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mckit_nuclides', 'mckit_nuclides.utils']

package_data = \
{'': ['*'], 'mckit_nuclides': ['data/*']}

install_requires = \
['multipledispatch>=0.6.0', 'numpy>=1.23.2', 'openpyxl>=3.0.9', 'pandas>=1.3.4']

setup_kwargs = {
    'name': 'mckit-nuclides',
    'version': '0.1.2',
    'description': '"Python tools to work with elements and isotopes"',
    'long_description': '==============================================================================\n*mckit-nuclides*: tables with information on elements and nuclides\n==============================================================================\n\n\n\n|Maintained| |License| |Versions| |PyPI| |Docs| |Bandit|\n\n.. contents::\n\n\nDescription\n-----------\n\nThe module presents basic information on chemical elements and nuclides organized as Pandas tables.\nThere are also some tools to work with composition fractions.\nPandas allows to use dataset approach on data indexing, joining and selecting.\n\nInstallation\n------------\n\n.. TODO\n\n\nExamples\n--------\n\n.. TODO\n\nContributing\n------------\n\n.. image:: https://github.com/MC-kit/mckit-nuclides/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/mckit-nuclides/actions?query=workflow%3ATests\n   :alt: Tests\n.. image:: https://codecov.io/gh/MC-kit/mckit-nuclides/branch/master/graph/badge.svg?token=wlqoa368k8\n  :target: https://codecov.io/gh/MC-kit/mckit-nuclides\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n   :target: https://pycqa.github.io/isort/\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\nReferences\n----------\n\n1. Kim, Sunghwan, Gindulyte, Asta, Zhang, Jian, Thiessen, Paul A. and Bolton, Evan E..\n   "PubChem Periodic Table and Element pages: improving access to information on chemical\n   elements from authoritative sources" Chemistry Teacher International, vol. 3, no. 1, 2021, pp. 57-65.\n   https://doi.org/10.1515/cti-2020-0006\n2. Elements table. https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV\n3. Coursey, J.S., Schwab, D.J., Tsai, J.J., and Dragoset, R.A. (2018-06-14),\n   Atomic Weights and Isotopic Compositions (version 4.1). [Online]\n   Available: http://physics.nist.gov/Comp [year, month, day].\n   National Institute of Standards and Technology, Gaithersburg, MD.\n\n\n.. Substitutions\n\n.. |Maintained| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n   :target: https://github.com/MC-kit/mckit-nuclides/graphs/commit-activity\n.. |Tests| image:: https://github.com/MC-kit/mckit-nuclides/workflows/Tests/badge.svg\n   :target: https://github.com/MC-kit/mckit-nuclides/actions?workflow=Tests\n   :alt: Tests\n.. |License| image:: https://img.shields.io/github/license/MC-kit/mckit-nuclides\n   :target: https://github.com/MC-kit/mckit-nuclides\n.. |Versions| image:: https://img.shields.io/pypi/pyversions/mckit-nuclides\n   :alt: PyPI - Python Version\n.. |PyPI| image:: https://img.shields.io/pypi/v/mckit-nuclides\n   :target: https://pypi.org/project/mckit-nuclides/\n   :alt: PyPI\n.. |Docs| image:: https://readthedocs.org/projects/mckit-nuclides/badge/?version=latest\n   :target: https://mckit-nuclides.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n.. |Bandit| image:: https://img.shields.io/badge/security-bandit-yellow.svg\n   :target: https://github.com/PyCQA/bandit\n   :alt: Security Status\n',
    'author': 'dvp',
    'author_email': 'dmitri_portnov@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MC-kit/mckit-nuclides',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
