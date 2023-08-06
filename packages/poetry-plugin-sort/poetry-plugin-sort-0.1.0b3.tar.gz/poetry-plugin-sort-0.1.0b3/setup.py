# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_sort']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['sort = '
                               'poetry_plugin_sort.plugins:SortDependenciesPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-sort',
    'version': '0.1.0b3',
    'description': 'Poetry plugin to sort the dependencies alphabetically',
    'long_description': '# Poetry Plugin: Dependencies sorting\n\n[![PyPI Version](https://img.shields.io/pypi/v/poetry-plugin-sort?label=PyPI)](https://pypi.org/project/poetry-plugin-sort/)\n\nThis package is a plugin that sort dependencies alphabetically in pyproject.toml\nafter running `poetry init`, `poetry add`, or `poetry remove`.\nSince [Introduce dependency sorting #3996](https://github.com/python-poetry/poetry/pull/3996) pull request still open\nthis plugin is a workaround for [!312](https://github.com/python-poetry/poetry/issues/312) issue.\n\n**Note**: the plugin is in the beta version!\n\n# Installation\n\nJust use `poetry self add` command to add this plugin.\n\n```bash\npoetry self add poetry-plugin-sort\n```\n\nIf you used pipx to install Poetry, add the plugin via `pipx inject` command.\n\n```bash\npipx inject poetry poetry-plugin-sort\n```\n\nAnd if you installed Poetry using pip, you can install the plugin the same way.\n\n```bash\npip install poetry poetry-plugin-sort\n```\n',
    'author': 'Andrei Shabanski',
    'author_email': 'shabanski.andrei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andrei-shabanski/poetry-plugin-sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
