# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmlt',
 'tmlt.core',
 'tmlt.core.domains',
 'tmlt.core.measurements',
 'tmlt.core.measurements.pandas_measurements',
 'tmlt.core.random',
 'tmlt.core.transformations',
 'tmlt.core.transformations.spark_transformations',
 'tmlt.core.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.0,<1.19.5',
 'pandas>=1.2.0,<2.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'pyspark[sql]>=3.0.0,<3.1.0',
 'python-flint==0.3.0',
 'randomgen>=1.18.1,<2.0.0',
 'scipy>=1.4.1,<1.6.1',
 'sympy>=1.8,<1.10',
 'typeguard>=2.12.1,<2.13.0',
 'typing_extensions>=3.10.0.0,<4.0.0.0']

setup_kwargs = {
    'name': 'tmlt.core',
    'version': '0.4.3',
    'description': "Tumult's differential privacy primitives",
    'long_description': '# Tumult Core\n\nTumult Core is a programming framework for implementing [differentially private](https://en.wikipedia.org/wiki/Differential_privacy) algorithms.\n\nThe design of Tumult Core is based on the design proposed in the [OpenDP White Paper](https://projects.iq.harvard.edu/files/opendifferentialprivacy/files/opendp_white_paper_11may2020.pdf), and can automatically verify the privacy properties of algorithms constructed from Tumult Core components. Tumult Core is scalable, includes a wide variety of components, and supports multiple privacy definitions.\n\n## Installation\n\nSee the [installation instructions in the documentation](https://docs.tmlt.dev/core/latest/installation.html#installation-instructions) for information about setting up prerequisites such as Spark and python-flint.\n\nOnce the prerequisites are installed, you can install Tumult Core using [pip](https://pypi.org/project/pip/).\n\n```bash\npip install tmlt.core\n```\n\n## Documentation\n\nThe full documentation is located at https://docs.tmlt.dev/core/latest.\n\n## Support\n\nIf you have any questions/concerns, please [create an issue](https://gitlab.com/tumult-labs/core/-/issues) or reach out to [support@tmlt.io](mailto:support@tmlt.io)\n\n## Contributing\n\nWe are not yet accepting external contributions, but please let us know at [support@tmlt.io](mailto:support@tmlt.io) if you are interested in contributing.\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md) for information about installing our development dependencies and running tests.\n\n\n## License\n\nCopyright Tumult Labs 2022\n\nThe Tumult Platform source code is licensed under the Apache License, version 2.0 (Apache-2.0).\nThe Tumult Platform documentation is licensed under\nCreative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA-4.0).\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tumult-labs/core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
