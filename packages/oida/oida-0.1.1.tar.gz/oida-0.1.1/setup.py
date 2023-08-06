# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oida', 'oida.checkers', 'oida.commands']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.4.3,<0.5.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=1.0.0']}

entry_points = \
{'console_scripts': ['oida = oida.console:main'],
 'flake8.extension': ['ODA = oida.flake8:Plugin']}

setup_kwargs = {
    'name': 'oida',
    'version': '0.1.1',
    'description': "Oida is Oda's linter that enforces code style and modularization in our Django projects.",
    'long_description': '<h1 align="center">\n  💅<br>\n  Oida\n</h1>\n\n<p align="center">\n  Oida is Oda\'s linter that enforces code style and modularization in our\n  Django projects.\n</p>\n\n> **Warning**\n> This project is still in early development. Expect breaking changes.\n\n## Installation\n\nOida requires Python 3.10 or newer and can be installed from\n[PyPI](https://pypi.org/project/oida):\n\n`pip install oida`\n\n## Usage\n\nOida is mainly intended to be used as a [flake8](https://flake8.pycqa.org/)\nplugin. Once you have installed Oida and flake8 you can enable the linting\nrules in the flake8 config:\n\n```ini\n[flake8]\nextend-select = ODA\n```\n\nThis will enable all our linting rules. You can also enable them one by one,\nfor a complete list of the various violations we report on see the\n[oida/checkers/base.py](oida/checkers/base.py) file.\n\nOida also provides its own command line tool. This can also be used to run the\nlinting rules, but its main purpose is to provide tools to help transitioning\nan existing codebase into one that\'s modularized. For details see `oida\n--help`, but below is a quick summary of the provided commands:\n\n### `oida lint`\n\nThis command is just another way of running the same checks that can be run\nthrough `flake8`. Note that this does not support `# noqa` comments.\n\n### `oida config`\n\nThis command will generate configuration files for components, which will be\nautomatically pre-filled with ignore rules for isolation violations. See below\nfor details on the configuration files.\n\n### `oida componentize`\n\nThis command moves or renames a Django app, for example for moving an app into\na component. In addition to moving the files in the app it also updates (or\nadds if needed) the app config and updates imports elsewhere in the project.\n\n\n## Concepts\n\nOida is a static code analyzer, that also looks at the project structure. The\ncodebase is expected to be structured with a project as the top package and\nthen Django apps or _components_ as submodules below this, something like this:\n\n    project/\n    ├── pyproject.toml\n    ├── setup.cfg\n    └── project/\n        ├── __init__.py\n        ├── my_component/\n        │   ├── __init__.py\n        │   ├── first_app/\n        │   │   ├── __init__.py\n        │   │   ├── models.py\n        │   │   └── ...\n        │   ├── second_app/\n        │   │   ├── __init__.py\n        │   │   └── ....\n        │   └── ...\n        ├── third_app/\n        │   ├── __init__.py\n        │   └── ...\n        └── ...\n\nA component is basically a collection of Django apps. Oida will enforce\nisolation of the apps inside the component, meaning that no code elsewhere in\nthe project will be allowed to import from the apps inside a component. Instead\na component should expose a public interface at the top level.\n\nBecause Oida is intended to be introduced in mature projects it\'s also possible\nto grandfather in existing violations. That\'s done through a `confcomponent.py`\nfile placed at the root of the component. The only allowed statement in this\nfile is assigning a list of string literals to `ALLOWED_IMPORTS`:\n\n```python\nALLOWED_IMPORTS = ["my_component.app.models.MyModel"]\n```\n\nThis will silence any warnings when importing `my_component.app.models.MyModel`\nin the current app/component.\n\n\n## Checks\n\nThese are the checks currently implemented in Oida:\n\n * **component-isolation:** Checks that relative imports do not cross app boundaries.\n * **config:** Checks that component configuration files are valid\n * **relative-imports:** Checks that no imports are done across components.\n',
    'author': 'Oda',
    'author_email': 'tech@oda.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kolonialno/oida',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
