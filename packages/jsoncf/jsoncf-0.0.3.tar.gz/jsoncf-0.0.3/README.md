# jsoncf

[![PyPI](https://img.shields.io/pypi/v/jsoncf)](https://img.shields.io/pypi/v/jsoncf)
[![Release](https://img.shields.io/github/v/release/idlewith/jsoncf?style=flat-square)](https://img.shields.io/github/v/release/idlewith/jsoncf?style=flat-square)
[![Python Versions](https://img.shields.io/pypi/pyversions/jsoncf?style=flat-square)](https://img.shields.io/pypi/pyversions/jsoncf?style=flat-square)
[![Commit activity](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)](https://img.shields.io/github/commit-activity/m/idlewith/jsoncf)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://idlewith.github.io/jsoncf/)
[![License](https://img.shields.io/github/license/idlewith/jsoncf)](https://img.shields.io/github/license/idlewith/jsoncf)

**prettify json string from clipboard**

- **Github repository**: <https://github.com/idlewith/jsoncf/>
- **Documentation** <https://idlewith.github.io/jsoncf/>


## Install

```shell
pip install jsoncf
```

## Usage

the json string below

```
{"employees":[  {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},  {"name":"Bob", "email":"bob32@gmail.com"},  {"name":"Jai", "email":"jai87@gmail.com"}  ]} 
```

you can select the whole json string, then type `Ctrl(Cmd) + C` to copy,

then just type the command

```shell
jsoncf
```

OR

you can use it as args

````shell
jsoncf '{"employees":[  {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},  {"name":"Bob", "email":"bob32@gmail.com"},  {"name":"Jai", "email":"jai87@gmail.com"}  ]} '
````

the output below

```json
{
 "employees": [
  {
   "name": "Shyam",
   "email": "shyamjaiswal@gmail.com"
  },
  {
   "name": "Bob",
   "email": "bob32@gmail.com"
  },
  {
   "name": "Jai",
   "email": "jai87@gmail.com"
  }
 ]
}
```


and `jsoncf` also write json data to `data.json` in current path


