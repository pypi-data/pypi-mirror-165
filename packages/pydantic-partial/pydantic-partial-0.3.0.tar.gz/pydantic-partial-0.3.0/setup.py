# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_partial']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-partial',
    'version': '0.3.0',
    'description': 'Create partial models from your pydantic models. Partial models may allow None for certain or all fields.',
    'long_description': "# `pydantic-partial`\n\nCreate partial models from your normal pydantic models. Partial models will allow\nsome or all fields to be optional and thus not be required when creating the model\ninstance.\n\nPartial models can be used to support PATCH HTTP requests where the suer only wants\nto update some fields of the model and normal validation for required fields is not\nrequired. It may also be used to have partial response DTO's where you want to skip\ncertain fields, this can be useful in combination with `exclude_none`. It is - like\nshown in these examples - intended to be used with API use cases, so when using\npydantic with for example FastAPI.\n\n**Disclaimer:** This is still an early release of `pydantic-partial`. Things might\nchange in the future. PR welcome. ;-)\n\n# Usage example\n\n`pydantic-partial` provides a mixin to generate partial model classes. The mixin can\nbe used like this:\n\n```python\nimport pydantic\nfrom pydantic_partial import PartialModelMixin\n\n# Something model, than can be used as a partial, too:\nclass Something(PartialModelMixin, pydantic.BaseModel):\n    name: str\n    age: int\n\n\n# Create a full partial model\nFullSomethingPartial = Something.as_partial()\nFullSomethingPartial(name=None, age=None)\n```\n\n## Without using the mixin mixin\n\nYou also may create partial models without using the mixin:\n\n```python\nimport pydantic\nfrom pydantic_partial import create_partial_model\n\n# Something model, without the mixin:\nclass Something(pydantic.BaseModel):\n    name: str\n    age: int\n\n\n# Create a full partial model\nFullSomethingPartial = create_partial_model(Something)\nFullSomethingPartial(name=None, age=None)\n```\n\n## Only changing some fields to being optional\n\n`pydantic-partial` can be used to create partial models that only change some\nof the fields to being optional. Just pass the list of fields to be optional to\nthe `as_partial()` or `create_partial_model()` function.\n\n```python\nimport pydantic\nfrom pydantic_partial import create_partial_model\n\nclass Something(pydantic.BaseModel):\n    name: str\n    age: int\n\n# Create a partial model only for the name attribute\nFullSomethingPartial = create_partial_model(Something, 'name')\nFullSomethingPartial(name=None)\n# This would still raise an error: FullSomethingPartial(age=None)\n```\n\n## Recursive partials\n\nPartial models can be created changing the field of all nested models to being\noptional, too.\n\n```python\nfrom typing import List\n\nimport pydantic\nfrom pydantic_partial import PartialModelMixin, create_partial_model\n\nclass InnerSomething(PartialModelMixin, pydantic.BaseModel):\n    name: str\n\nclass OuterSomething(pydantic.BaseModel):\n    name: str\n    things: List[InnerSomething]\n\n# Create a full partial model\nRecursiveOuterSomethingPartial = create_partial_model(OuterSomething, recursive=True)\nRecursiveOuterSomethingPartial(things=[\n    {},\n])\n```\n\n**Note:** The inner model MUST extend the `PartialModelMixin` mixin. Otherwise\n`pydantic-partial` will not be able to detect which fields may allow to being\nconverted to partial models.\n\n**Also note:** My recommendation would be to always create such recursive\npartials by creating partials for all the required models and then override\nthe fields on you outer partial model class. This is way more explicit.\n\n# Contributing\n\nIf you want to contribute to this project, feel free to just fork the project,\ncreate a dev branch in your fork and then create a pull request (PR). If you\nare unsure about whether your changes really suit the project please create an\nissue first, to talk about this.\n",
    'author': 'TEAM23 GmbH',
    'author_email': 'info@team23.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/team23/pydantic-partial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
