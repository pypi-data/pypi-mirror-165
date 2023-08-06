# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edspdf',
 'edspdf.aggregators',
 'edspdf.classifiers',
 'edspdf.extractors',
 'edspdf.extractors.style',
 'edspdf.misc',
 'edspdf.readers',
 'edspdf.transforms',
 'edspdf.visualization']

package_data = \
{'': ['*']}

install_requires = \
['catalogue>=2.0.7,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'networkx>=2.6,<3.0',
 'pandas>=1.2,<2.0',
 'pdfminer.six>=20220319,<20220320',
 'pydantic>=1.2,<2.0',
 'pypdfium2>=2.7.1,<3.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'thinc>=8.0.15,<9.0.0']

setup_kwargs = {
    'name': 'edspdf',
    'version': '0.5.2',
    'description': 'Smart text extraction from PDF documents',
    'long_description': '![Tests](https://img.shields.io/github/workflow/status/aphp/edspdf/Tests%20and%20Linting?label=tests&style=flat-square)\n[![Documentation](https://img.shields.io/github/workflow/status/aphp/edspdf/Documentation?label=docs&style=flat-square)](https://aphp.github.io/edspdf/latest/)\n[![PyPI](https://img.shields.io/pypi/v/edspdf?color=blue&style=flat-square)](https://pypi.org/project/edspdf/)\n[![Codecov](https://img.shields.io/codecov/c/github/aphp/edspdf?logo=codecov&style=flat-square)](https://codecov.io/gh/aphp/edspdf)\n[![DOI](https://zenodo.org/badge/517726737.svg)](https://zenodo.org/badge/latestdoi/517726737)\n\n# EDS-PDF\n\nEDS-PDF provides modular framework to extract text from PDF documents.\n\nYou can use it out-of-the-box, or extend it to fit your use-case.\n\n## Getting started\n\nInstall the library with pip:\n\n<div class="termy">\n\n```console\n$ pip install edspdf\n```\n\n</div>\n\nVisit the [documentation](https://aphp.github.io/edspdf/) for more information!\n\n## Citation\n\nIf you use EDS-NLP, please cite us as below.\n\n```bibtex\n@software{edspdf,\n  author  = {Dura, Basile and Wajsburt, Perceval and Calliger, Alice and Gérardin, Christel and Bey, Romain},\n  doi     = {10.5281/zenodo.6902977},\n  license = {BSD-3-Clause},\n  title   = {{EDS-PDF: Smart text extraction from PDF documents}},\n  url     = {https://github.com/aphp/edspdf}\n}\n```\n\n## Acknowledgement\n\nWe would like to thank [Assistance Publique – Hôpitaux de Paris](https://www.aphp.fr/)\nand [AP-HP Foundation](https://fondationrechercheaphp.fr/) for funding this project.\n',
    'author': 'Basile Dura',
    'author_email': 'basile.dura-ext@aphp.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aphp/edspdf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
