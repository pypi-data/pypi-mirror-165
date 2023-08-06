# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['option']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'option-python',
    'version': '0.0.1',
    'description': 'A simple Rust-like Option type for Python with Type Annotations',
    'long_description': "# Option\nA simple Rust-like Option type for Python with Type Annotations.\n\nThis package is heavily based on the [Result](https://github.com/rustedpy/result) package's implementation.\n\n## Installation\n```\npip install option-python\n```\n",
    'author': 'Catminusminus',
    'author_email': 'getomya@svk.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Catminusminus/option',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
