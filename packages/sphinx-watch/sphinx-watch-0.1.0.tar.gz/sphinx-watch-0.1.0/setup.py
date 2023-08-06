# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_watch']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx', 'click', 'watchdog']

entry_points = \
{'console_scripts': ['sphinx-watch = sphinx_watch.cli:main']}

setup_kwargs = {
    'name': 'sphinx-watch',
    'version': '0.1.0',
    'description': 'Helper CLI for Sphinx to realtime build',
    'long_description': '============\nsphinx-watch\n============\n\nThis is CLI tool for Documentation eXperimence with Sphinx.\n\nOverview\n========\n\n``sphinx-watch`` provides these features for user local environment.\n\n* Build document of Sphinx when source files are changed by users\n* HTTP server to publish built documentation using ``http.server``\n\nInstallation\n============\n\nUploaded PyPI\n\n.. code-block::\n\n   pip install sphinx-watch\n\nUsage\n=====\n\nBuild only\n\n.. code-block:: console\n\n   sphinx-watch source build html\n\nRun HTTP server\n\n.. code-block:: console\n\n   sphinx-watch source build html --http\n\nSpecify port by running HTTP server\n\n.. code-block:: console\n\n   sphinx-watch source build html --http --port 8080\n\nDevelopment\n===========\n\nThis uses ``poetry`` and ``pre-commit``\n\n.. code-block:: console\n\n   git clone\n   cd sphinx-watch\n   poetry install\n   pre-commit install\n\nLicense\n=======\n\nApache License 2.0\n',
    'author': 'Kazuya Takei',
    'author_email': 'myself@attakei.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/attakei-lab/sphinx-watch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
