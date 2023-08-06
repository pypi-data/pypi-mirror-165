# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaphid']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0', 'tomli>=2.0.1,<3.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pyaphid = pyaphid.cli:run']}

setup_kwargs = {
    'name': 'pyaphid',
    'version': '0.1.0',
    'description': 'Identify and remove debugging code',
    'long_description': '# Pyaphid\n\nPyaphid is a tool for detecting unwanted function calls in Python code.\n\n## Installation and usage\n\nInstallation: `pip install pyaphid`\n\nUsage: `python -m pyaphid <files and/or directories to analyze>` or `pyaphid <files and/or directories to analyze>`\n\n### Configuration\n\nForbidden function calls can be configured via the `pyproject.toml`:\n\n```toml\n[tool.pyaphid]\nforbidden = [\n    "print",\n    "pdb.run",\n    "werkzeug.debug.*"\n]\n```\n\n### CLI Options\n\n- -n / --names: `Look-up all func calls and print their identifier`\n\n## Limitations\n\n```python\n# Pyaphid cannot work with star imports\nfrom os.path import *\ndirname(".") # undetected\n\n# Pyaphid doesn\'t track assignments\nmy_print = print\nmy_print("Hello world") # undetected\n```\n',
    'author': 'Jan Vollmer',
    'author_email': 'jan@vllmr.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jvllmr/pyaphid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
