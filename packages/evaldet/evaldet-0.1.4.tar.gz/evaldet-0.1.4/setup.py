# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evaldet', 'evaldet.mot_metrics', 'evaldet.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.2,<2.0.0', 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'evaldet',
    'version': '0.1.4',
    'description': 'Evaluation for Detection and Tracking',
    'long_description': '# EvalDeT\n\nEvaluation for Detection and Tracking\n',
    'author': 'Tadej Svetina',
    'author_email': 'tadej.svetina@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tadejsv/evaldet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
