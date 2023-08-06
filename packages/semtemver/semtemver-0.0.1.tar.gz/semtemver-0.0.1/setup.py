# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['semtemver']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['semtemver = semtemver.__main__:main']}

setup_kwargs = {
    'name': 'semtemver',
    'version': '0.0.1',
    'description': '',
    'long_description': '# semtemver\nplaying with semantic versioning and publishing\n',
    'author': 'dskard',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
