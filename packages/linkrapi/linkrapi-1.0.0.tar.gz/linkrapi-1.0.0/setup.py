# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['linkrpy']
install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'linkrapi',
    'version': '1.0.0',
    'description': 'Make short links in seconds! With LinkR API',
    'long_description': '# LinkR.py - Make short links in seconds!\nAn API wrapper for LinkR\n\n# Example\n```linkr = LinkR(key = "your_api_key")```\n\n```linkr.generate("https://example.com")```',
    'author': 'DragonFire0159x',
    'author_email': 'prosdenis1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
