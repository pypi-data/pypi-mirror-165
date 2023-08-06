# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_choices_field']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-choices-field',
    'version': '2.1',
    'description': "Django field that set/get django's new TextChoices/IntegerChoices enum.",
    'long_description': '# django-choices-field\n\n[![build status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbellini666%2Fdjango-choices-field%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/bellini666/django-choices-field/goto?ref=master)\n[![coverage](https://img.shields.io/codecov/c/github/bellini666/django-choices-field.svg)](https://codecov.io/gh/bellini666/django-choices-field)\n[![PyPI version](https://img.shields.io/pypi/v/django-choices-field.svg)](https://pypi.org/project/django-choices-field/)\n![python version](https://img.shields.io/pypi/pyversions/django-choices-field.svg)\n![django version](https://img.shields.io/pypi/djversions/django-choices-field.svg)\n\nDjango field that set/get django\'s new TextChoices/IntegerChoices enum.\n\n## Install\n\n```bash\npip install django-choices-field\n```\n\n## Usage\n\n```python\nfrom django.db import models\nfrom django_choices_field import TexChoicesField, IntegerChoicesField\n\n\nclass MyModel(models.Model):\n    class TextEnum(models.TextChoices):\n        FOO = "foo", "Foo Description"\n        BAR = "bar", "Bar Description"\n\n    class IntegerEnum(models.IntegerChoices):\n        FIRST = 1, "First Description"\n        SECOND = 2, "Second Description"\n\n    c_field = TextChoicesField(\n        choices_enum=TextEnum,\n        default=TextEnum.FOO,\n    )\n    i_field = IntegerChoicesField(\n        choices_enum=IntegerEnum,\n        default=IntegerEnum.FIRST,\n    )\n\n\nobj = MyModel()\nobj.c_field  # MyModel.TextEnum.FOO\nisinstance(obj.c_field, MyModel.TextEnum) # True\nobj.i_field  # MyModel.IntegerEnum.FIRST\nisinstance(obj.i_field, MyModel.IntegerEnum) # True\n```\n\n## License\n\nThis project is licensed under MIT licence (see `LICENSE` for more info)\n\n## Contributing\n\nMake sure to have [poetry](https://python-poetry.org/) installed.\n\nInstall dependencies with:\n\n```bash\npoetry install\n```\n\nRun the testsuite with:\n\n```bash\npoetry run pytest\n```\n\nFeel free to fork the project and send me pull requests with new features,\ncorrections and translations. I\'ll gladly merge them and release new versions\nASAP.\n',
    'author': 'Thiago Bellini Ribeiro',
    'author_email': 'thiago@bellini.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bellini666/django-choices-field',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
