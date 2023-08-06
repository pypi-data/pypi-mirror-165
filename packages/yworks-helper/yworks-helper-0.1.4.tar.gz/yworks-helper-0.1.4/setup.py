# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yworks_helper',
 'yworks_helper.core',
 'yworks_helper.core.bp',
 'yworks_helper.core.dmo',
 'yworks_helper.core.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'ipykernel', 'jupyter>=1.0.0,<2.0.0', 'yfiles_jupyter_graphs']

setup_kwargs = {
    'name': 'yworks-helper',
    'version': '0.1.4',
    'description': 'Helper Microservice to create yWorks Graphs in Jupyter',
    'long_description': None,
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
