# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyscript', 'pyscript.plugins']

package_data = \
{'': ['*'], 'pyscript': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'pluggy>=1.0.0,<2.0.0',
 'rich-click[typer]>=1.3.0,<2.0.0',
 'rich>=12.3.0,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{':python_version == "3.7"': ['importlib-metadata>=4.11.3,<5.0.0'],
 'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-autodoc-typehints>=1.19.2,<2.0.0',
          'myst-parser>=0.18.0,<0.19.0',
          'pydata-sphinx-theme>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['pyscript = pyscript.cli:app']}

setup_kwargs = {
    'name': 'pyscript',
    'version': '0.2.2',
    'description': 'Command Line Interface for PyScript',
    'long_description': '# PyScript CLI\n\nA command-line interface for [PyScript](https://pyscript.net).\n\n\n[![Version](https://img.shields.io/pypi/v/pyscript.svg)](https://pypi.org/project/pyscript/)\n[![Test](https://github.com/pyscript/pyscript-cli/actions/workflows/test.yml/badge.svg)](https://github.com/pyscript/pyscript-cli/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/pyscript/pyscript-cli/branch/main/graph/badge.svg?token=dCxt9oBQPL)](https://codecov.io/gh/pyscript/pyscript-cli)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pyscript/pyscript-cli/main.svg)](https://results.pre-commit.ci/latest/github/pyscript/pyscript-cli/main)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nQuickly wrap Python scripts into a HTML template, pre-configured with [PyScript](https://pyscript.net).\n\n<img src="https://user-images.githubusercontent.com/11037737/166966219-9440c3cc-e911-4730-882c-2ab9fa47147f.gif" style="width: 100%; max-width: 680px;" />\n\n## Installation\n\n```shell\n$ pip install pyscript\n```\n\n## Usage\n\n### Embed a Python script into a PyScript HTML file\n\n```shell\n$ pyscript wrap <filename.py>\n```\n\nThis will generate a file called `<filename.html>` by default.\nThis can be overwritten with the `-o` or `--output` option:\n\n```shell\n$ pyscript wrap <filename.py> -o <another_filename.html>\n```\n\n### Open the script inside the browser using the `--show` option\n\n```shell\n$ pyscript wrap <filename.py> --show\n```\n\n### Set a title for the browser tab\n\nYou can set the title of the browser tab with the `--title` option:\n\n```shell\n$ pyscript wrap <filename.py> --title "My cool app!"\n```\n\n### Very simple command examples with `--command` option\n\nThe `-c` or `--command` option can be used to demo very simple cases.\nIn this case, if the `--show` option is used and no `--output` file is used, a temporary file will be generated.\n\n```shell\n$ pyscript wrap -c \'print("Hello World!")\' --show\n```\n',
    'author': 'Matt Kramer',
    'author_email': 'mkramer@anaconda.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyscript/pyscript-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
