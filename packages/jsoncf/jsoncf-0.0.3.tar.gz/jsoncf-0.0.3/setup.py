# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jsoncf']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'jsoncf',
    'version': '0.0.3',
    'description': 'prettify json data from clipboard',
    'long_description': '# jsoncf\n\n[![PyPI](https://img.shields.io/pypi/v/jsoncf)](https://img.shields.io/pypi/v/jsoncf)\n[![Release](https://img.shields.io/github/v/release/idlewith/jsoncf?style=flat-square)](https://img.shields.io/github/v/release/idlewith/jsoncf?style=flat-square)\n[![Python Versions](https://img.shields.io/pypi/pyversions/jsoncf?style=flat-square)](https://img.shields.io/pypi/pyversions/jsoncf?style=flat-square)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://idlewith.github.io/jsoncf/)\n[![License](https://img.shields.io/github/license/idlewith/jsoncf)](https://img.shields.io/github/license/idlewith/jsoncf)\n\n**prettify json string from clipboard**\n\n- **Github repository**: <https://github.com/idlewith/jsoncf/>\n- **Documentation** <https://idlewith.github.io/jsoncf/>\n\n\n## Install\n\n```shell\npip install jsoncf\n```\n\n## Usage\n\nthe json string below\n\n```\n{"employees":[  {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},  {"name":"Bob", "email":"bob32@gmail.com"},  {"name":"Jai", "email":"jai87@gmail.com"}  ]} \n```\n\nyou can select the whole json string, then type `Ctrl(Cmd) + C` to copy,\n\nthen just type the command\n\n```shell\njsoncf\n```\n\nOR\n\nyou can use it as args\n\n````shell\njsoncf \'{"employees":[  {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},  {"name":"Bob", "email":"bob32@gmail.com"},  {"name":"Jai", "email":"jai87@gmail.com"}  ]} \'\n````\n\nthe output below\n\n```json\n{\n "employees": [\n  {\n   "name": "Shyam",\n   "email": "shyamjaiswal@gmail.com"\n  },\n  {\n   "name": "Bob",\n   "email": "bob32@gmail.com"\n  },\n  {\n   "name": "Jai",\n   "email": "jai87@gmail.com"\n  }\n ]\n}\n```\n\n\nand `jsoncf` also write json data to `data.json` in current path\n\n\n',
    'author': 'idlewith',
    'author_email': 'newellzhou@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
