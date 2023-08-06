# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_apply']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0']

setup_kwargs = {
    'name': 'pydantic-apply',
    'version': '0.1.0',
    'description': 'Apply changes as patches to pydanic models.',
    'long_description': '# pydantic-apply\n\nWith `pydantic-apply` you can apply changes to your pydantic models by using\nthe `ApplyModelMixin` it provides:\n\n```python\nimport pydantic\n\nfrom pydantic_apply import ApplyModelMixin\n\n\nclass Something(ApplyModelMixin, pydantic.BaseModel):\n    name: str\n    age: int\n\n\nobj = Something(name=\'John Doe\', age=42)\nobj.apply({\n    "age": 43,\n})\nassert obj.age == 43\n```\n\nAs the apply data you may pass any dictionary or other pydanic object as you\nwish. pydantic objects will be converted to dict\'s when being applied - but will\nonly use fields that where explicitly set on the model instance. Also note\nthat `.apply()` will ignore all fields not present in the model, like the\nmodel constructor would.\n\n## Nested models\n\n`pydantic-apply` will also know how to apply changes to nested models. If those\nmodels are by themself subclasses of `ApplyModelMixin` it will call `apply()`\non those fields as well. Otherwise the whole attribute will be replaced.\n\n## Apply changes when using `validate_assignment`\n\nWhen your models have `validate_assignment` enabled it may become tricky to\napply changes to the model. This is due to the fact that you only can assign\nfields once at a time. But with `validate_assignment` enabled this means each\nfield assignment will trigger its own validation and this validation might\nfail as the model state is not completely changes and thus in a "broken"\nintermediate state.\n\n`pydantic-apply` will take care of this issue and disable the validation for\neach assignment while applying the changes. It will also ensure the resulting\nobject will still pass the validation, so you don\'t have to care about this\ncase at all.\n\n# Contributing\n\nIf you want to contribute to this project, feel free to just fork the project,\ncreate a dev branch in your fork and then create a pull request (PR). If you\nare unsure about whether your changes really suit the project please create an\nissue first, to talk about this.\n',
    'author': 'TEAM23 GmbH',
    'author_email': 'info@team23.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/team23/pydantic-apply',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
