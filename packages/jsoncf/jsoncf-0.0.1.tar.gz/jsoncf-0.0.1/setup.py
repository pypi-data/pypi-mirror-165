# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsoncf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsoncf',
    'version': '0.0.1',
    'description': 'prettify json string from clipboard',
    'long_description': '# jsoncf\n\n[![Release](https://img.shields.io/github/v/release/idlewith/jsoncf)](https://img.shields.io/github/v/release/idlewith/jsoncf)\n[![Build status](https://img.shields.io/github/workflow/status/idlewith/jsoncf/merge-to-main)](https://img.shields.io/github/workflow/status/idlewith/jsoncf/merge-to-main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://idlewith.github.io/jsoncf/)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![License](https://img.shields.io/github/license/idlewith/jsoncf)](https://img.shields.io/github/license/idlewith/jsoncf)\n\nprettify json string from clipboard\n\n- **Github repository**: <https://github.com/idlewith/jsoncf/>\n- **Documentation** <https://idlewith.github.io/jsoncf/>\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting \n[this page](https://github.com/idlewith/jsoncf/settings/secrets/actions/new).\n- Create a [new release](https://github.com/idlewith/jsoncf/releases/new) on Github. \nCreate a new tag in the form ``*.*.*``.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/releasing.html).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).',
    'author': 'idlewith',
    'author_email': 'fnewellzhou@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/idlewith/jsoncf',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
