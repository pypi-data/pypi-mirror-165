# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['narca']

package_data = \
{'': ['*']}

install_requires = \
['griddly>=1.4',
 'gym==0.22.0',
 'icecream>=2.1',
 'matplotlib>=3.2',
 'neptune-client>=0.16',
 'numpy>=1.17',
 'pyglet>=1.3',
 'tensorboard>=2.9',
 'tensorboardX>=2.5']

setup_kwargs = {
    'name': 'narca',
    'version': '0.1.0',
    'description': 'NARS Controlled Agent: an agent capable of playing various games in Gym environments, using NARS for planning.',
    'long_description': None,
    'author': 'Adrian Borucki',
    'author_email': 'ab@synthillect.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
