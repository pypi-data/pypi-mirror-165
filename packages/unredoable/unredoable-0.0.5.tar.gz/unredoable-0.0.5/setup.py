# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unredoable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unredoable',
    'version': '0.0.5',
    'description': 'Object-specific undoing and redoing functionality through wrapper class',
    'long_description': "# __unredoable__\nPython package providing object-specific undoing & redoing functionality through wrapper class\n\n[![Build](https://github.com/w2sv/unredoable/actions/workflows/build.yaml/badge.svg)](https://github.com/w2sv/unredoable/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/w2sv/unredoable/branch/master/graph/badge.svg?token=9EESND69PG)](https://codecov.io/gh/w2sv/unredoable)\n[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)\n![PyPI](https://img.shields.io/pypi/v/unredoable)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n\n## Download\n```\npip install unredoable\n```\n\n## Usage\n\n```python\nfrom unredoable import Unredoable\n\nclass StateManager:\n    def __init__(self, state_variable):\n        self.unredoable_state_variable = Unredoable(state_variable, max_stack_depths=10, craft_deep_copies=False)\n        \n        # state_variable may be of whatever type, whether custom or not, \n        # the sole restraint it's subject to, is that is needs to implement \n        # either __copy__ or __deepcopy__, depending on the passed \n        # 'craft_deep_copies' parameter\n        \n    def alter_state_variable(self):\n        self.unredoable_state_variable.push_state()\n        \n        self.unredoable_state_variable.obj += 1\n\nif __name__ == '__main__':\n    manager = StateManager(69)\n    \n    manager.alter_state_variable()\n    manager.alter_state_variable()\n    \n    manager.unredoable_state_variable.undo()  # unredoable_state_variable = 70\n    manager.unredoable_state_variable.redo()  # unredoable_state_variable = 71\n```\n\n\n## Author\nJanek Zangenberg\n\n## License\n[MIT](LICENSE)\n",
    'author': 'w2sv',
    'author_email': 'zangenbergjanek@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/w2sv/monostate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
