# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_changedetect']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0']

setup_kwargs = {
    'name': 'pydantic-changedetect',
    'version': '0.2.1',
    'description': 'Extend pydantic models to also detect and record changes made to the model attributes.',
    'long_description': '# Pydantic change detection\n\nWhen working with database models it is pretty common to want to detect changes\nto the model attributes. The `ChangeDetectionMixin` just provides this mechanism\nto any pydantic models. Changes will be detected and stored after the model\nwas constructed.\n\nUsing the `ChangeDetectionMixin` the pydantic models are extended, so:\n* `obj.__changed_fields__` contains a list of all changed fields\n  - `obj.__self_changed_fields__` contains a list of all changed fields for the\n    current object, ignoring all nested models.\n  - `obj.__changed_fields_recursive__` contains a list of all changed fields and\n    also include the named of the fields changed in nested models using a\n    dotted field name syntax (like `nested.field`).\n* `obj.__original__` will include the original values of all changed fields in\n  a dict.\n* `obj.has_changed()` returns True if any field has changed.\n* `obj.set_changed()` manually sets fields as changed.\n  - `obj.set_changed("field_a", "field_b")` will set multiple fields as changed.\n  - `obj.set_changed("field_a", original="old")` will set a single field as\n    changed and also store its original value.\n* `obj.reset_changed()` resets all changed fields.\n* `obj.dict()` and `obj.json()` accept an additional parameter\n  `exclude_unchanged`, which - when set to True - will only export the\n  changed fields\n\n## Example\n\n```python\nimport pydantic\nfrom pydantic_changedetect import ChangeDetectionMixin\n\nclass Something(ChangeDetectionMixin, pydantic.BaseModel):\n    name: str\n\n\nsomething = Something(name="something")\nsomething.has_changed  # = False\nsomething.__changed_fields__  # = set()\nsomething.name = "something else"\nsomething.has_changed  # = True\nsomething.__changed_fields__  # = {"name"}\n```\n\n## Restrictions\n\n`ChangeDetectionMixin` currently cannot detect changes inside lists, dicts and\nother structured objects. In those cases you are required to set the changed\nstate yourself using `set_changed()`. It is recommended to pass the original\nvalue to `set_changed()` when you want to also keep track of the actual changes\ncompared to the original value. Be advised to `.copy()` the original value\nas lists/dicts will always be changed in place.\n\n# Contributing\n\nIf you want to contribute to this project, feel free to just fork the project,\ncreate a dev branch in your fork and then create a pull request (PR). If you\nare unsure about whether your changes really suit the project please create an\nissue first, to talk about this.\n',
    'author': 'TEAM23 GmbH',
    'author_email': 'info@team23.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/team23/pydantic-changedetect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
