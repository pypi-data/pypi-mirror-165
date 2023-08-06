# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpytorch', 'jrpytorch.datasets']

package_data = \
{'': ['*'], 'jrpytorch': ['vignettes/*'], 'jrpytorch.datasets': ['data/*']}

install_requires = \
['matplot>=0.1.9,<0.2.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'visdom>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'jrpytorch',
    'version': '0.2.0',
    'description': 'Jumping Rivers: PyTorch with Python',
    'long_description': None,
    'author': 'Jumping Rivers',
    'author_email': 'info@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
