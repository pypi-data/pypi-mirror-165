# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_types', 'poetry_types.commands']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2,<2.0']

entry_points = \
{'poetry.application.plugin': ['poetry-types = '
                               'poetry_types.poetry_types:PoetryTypes']}

setup_kwargs = {
    'name': 'poetry-types',
    'version': '0.3.1',
    'description': 'A poetry plugin that adds/removes type stubs as dependencies like the mypy --install-types command.',
    'long_description': '\n# poetry-types\n\nThis is a plugin to poetry for the upcoming poetry 1.2 plugin feature.\nIt installs/removes/updates typing stubs via following commands:\n\n- `poetry types add <package names>`\n- `poetry types remove <package names>`\n- `poetry types update <package names>`\n\n## Usage examples\n\n- `poetry types add SQLAlchemy` adds `types-SQLAlchemy` to your project\n- `poetry types update` adds `types-SQLAlchemy` if `SQLAlchemy` is present, but not `types-SQLAlchemy`\n- `poetry types update` removes `types-SQLAlchemy` if `types-SQLAlchemy` is present, but not `SQLAlchemy`\n\n## Installation\n\nRun `poetry plugin add poetry-types` for global install or run `poetry add -D poetry-types` to use this plugin with your project.\n',
    'author': 'Jan Vollmer',
    'author_email': 'jan@vllmr.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jvllmr/poetry-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
