# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyreqpp', 'pyreqpp.utils']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.4,<0.12.0', 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'pyreqpp',
    'version': '0.1.0',
    'description': "Takes requirements.txt file without module versions and annotates it with the latest set of module versions that won't result in build/runtime errors.",
    'long_description': None,
    'author': 'sudomaze',
    'author_email': 'sudomaze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sudomaze/pyreqpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.13,<4.0.0',
}


setup(**setup_kwargs)
