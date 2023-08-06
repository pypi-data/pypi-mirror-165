# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enopios']

package_data = \
{'': ['*']}

install_requires = \
['streamlit']

entry_points = \
{'console_scripts': ['enopios = enopios.__main__:app']}

setup_kwargs = {
    'name': 'enopios',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Simon Biggs',
    'author_email': 'simon.biggs@radiotherapy.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
