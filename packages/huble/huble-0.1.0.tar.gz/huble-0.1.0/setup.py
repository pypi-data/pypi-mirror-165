# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['huble',
 'huble.sklearn',
 'huble.sklearn.automl',
 'huble.sklearn.deploy',
 'huble.sklearn.process',
 'huble.sklearn.train',
 'huble.util']

package_data = \
{'': ['*'], 'huble.sklearn': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'black>=22.8.0,<23.0.0',
 'pandas>=1.4.4,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'huble',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Rugz007',
    'author_email': 'rugvedsomwanshi007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
