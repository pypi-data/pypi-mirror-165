# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['material_color_utilities_python',
 'material_color_utilities_python.blend',
 'material_color_utilities_python.hct',
 'material_color_utilities_python.palettes',
 'material_color_utilities_python.quantize',
 'material_color_utilities_python.scheme',
 'material_color_utilities_python.score',
 'material_color_utilities_python.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0', 'regex']

setup_kwargs = {
    'name': 'material-color-utilities-python',
    'version': '0.1.5',
    'description': 'Python port of material-color-utilities used for Material You colors',
    'long_description': None,
    'author': 'Avanish Subbiah',
    'author_email': 'avanishsubbiah1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
