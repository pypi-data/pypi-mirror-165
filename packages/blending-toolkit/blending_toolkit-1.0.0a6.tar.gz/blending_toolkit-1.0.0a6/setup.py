# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btk']

package_data = \
{'': ['*']}

install_requires = \
['galcheat>=1.0.0',
 'galsim>=2.3.5',
 'ipywidgets>=7.6.5',
 'matplotlib>=3.5.1',
 'scikit-image>=0.19.2',
 'seaborn>=0.11.2',
 'sep>=1.2.0',
 'tqdm>=4.64.0']

extras_require = \
{':python_full_version >= "3.7.1" and python_full_version < "3.8.0"': ['astropy>=4.3.1,<5.0.0',
                                                                       'numpy>=1.16.5,<1.22.0',
                                                                       'pandas>=1.3.5,<1.4.0',
                                                                       'scipy>=1.7.3,<1.8.0'],
 ':python_version >= "3.8"': ['astropy>=5.1',
                              'numpy>=1.22',
                              'pandas>=1.4.2',
                              'scipy>=1.8.1']}

setup_kwargs = {
    'name': 'blending-toolkit',
    'version': '1.0.0a6',
    'description': 'Blending ToolKit',
    'long_description': '# BlendingToolKit\n\n![tests](https://github.com/LSSTDESC/BlendingToolKit/workflows/tests/badge.svg)\n![tests](https://github.com/LSSTDESC/BlendingToolKit/workflows/docs/badge.svg)\n[![notebooks](https://github.com/LSSTDESC/BlendingToolKit/actions/workflows/notebooks.yml/badge.svg?branch=main)](https://github.com/LSSTDESC/BlendingToolKit/actions/workflows/notebooks.yml)\n[![codecov](https://codecov.io/gh/LSSTDESC/BlendingToolKit/branch/main/graph/badge.svg)](https://codecov.io/gh/LSSTDESC/BlendingToolKit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![PyPI][pypi-badge]][pypi]\n\n[pypi-badge]: <https://img.shields.io/pypi/pyversions/blending-toolkit?color=yellow&logo=pypi>\n[pypi]: <https://pypi.org/project/blending-toolkit/>\n\n## Summary\n\nFramework for fast generation and analysis of galaxy blends catalogs. This toolkit is a convenient way of\nproducing multi-band postage stamp images of blend scenes.\n\nDocumentation can be found at <https://lsstdesc.org/BlendingToolKit/index.html>\n\n## Workflow\n\n<img src="docs/source/images/diagram.png" alt="btk workflow" width="550"/>\n\n- In red are the BTK objects that can be customized in various ways by BTK users.\n\n## Running BlendingToolKit\n\n- BlendingToolKit (btk) requires an input catalog that contains information required to simulate galaxies and blends.\nThis repository includes sample input catalogs with a small number of galaxies that can be used to draw blend images with btk. See [tutorials](https://github.com/LSSTDESC/BlendingToolKit/tree/main/notebooks) to learn how to run btk with these catalogs.\n- CatSim Catalog corresponding to one square degree of sky and processed WeakLensingDeblending catalogs can be downloaded from [here](https://stanford.app.box.com/s/s1nzjlinejpqandudjyykjejyxtgylbk).\n- [Cosmo DC2](https://arxiv.org/abs/1907.06530) catalog requires pre-processing in order to be used as input catalog to btk. Refer to this [notebook](https://github.com/LSSTDESC/WeakLensingDeblending/blob/cosmoDC2_ingestion/notebooks/wld_ingestion_cosmoDC2.ipynb) on how to convert the DC2 catalog into a CatSim-like catalog that can be analyzed with btk.\n\n## Installation\n\nBTK is pip installable, with the following command:\n\n```bash\npip install blending_toolkit\n```\n\nAlthough you might run into problems installing `galsim`. In case of any issues, please see the more detailed installation instructions [here](https://lsstdesc.org/BlendingToolKit/install.html).\n\nFor required packages, see [pyproject.toml](https://github.com/LSSTDESC/BlendingToolKit/blob/main/pyproject.toml) under the `[tool.poetry.dependencies]` block. For developers, you will also need the packages under the `[tool.poetry.dev-dependencies]` block.\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/LSSTDESC/BlendingToolKit/blob/main/CONTRIBUTING.md)\n',
    'author': 'Ismael Mendoza',
    'author_email': 'imendoza@umich.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LSSTDESC/BlendingToolKit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10.0',
}


setup(**setup_kwargs)
