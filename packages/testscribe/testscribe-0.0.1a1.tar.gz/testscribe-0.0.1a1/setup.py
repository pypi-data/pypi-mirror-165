# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testscribe', 'testscribe.api']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.2', 'typer']

setup_kwargs = {
    'name': 'testscribe',
    'version': '0.0.1a1',
    'description': 'Unit test automation tool',
    'long_description': '# TestScribe for Python\n\nUnit test made easy\n\nA tool to make python unit testing easier by automating the boring and repetitive parts.\n\n',
    'author': 'Ray Yang',
    'author_email': 'ruiguo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
