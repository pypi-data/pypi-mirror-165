# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rxio']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform != "win32" and implementation_name == "cpython"': ['uvloop>=0.16,<0.17']}

setup_kwargs = {
    'name': 'rxio',
    'version': '0.1.1',
    'description': 'Flexible, predictable, async reactive programming in modern Python',
    'long_description': '# Reactive I/O\n\n-----\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/rxio.svg)](https://pypi.python.org/pypi/rxio/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/rxio.svg)](https://pypi.python.org/pypi/rxio/)\n[![PyPI license](https://img.shields.io/pypi/l/rxio.svg)](https://pypi.python.org/pypi/rxio/)\n\n-----\n\nCurrently in the early development phase; do not use in production.\n\n\n## Roadmap:\n\n- [x] `RxVar[T]`: variable\n- [ ] `RxResult[*Ps, T]`: function result, bound to reactive args\n- [ ] `Rx{Function,Method}`: returns `RxResult`, can watch when called\n- [ ] (mk)docs \n- [ ] github actions\n- [ ] `RxAttr[T]`: descriptor attribute / field\n- [ ] `RxType`: custom rx type base: reactive attrs, methods, properties and lifecycle\n- [ ] `Rx{Bool,Int,Float,Str,...}`: reactie builtin types\n- [ ] `Rx{Tuple,List,Set,Dict,...}`: reactive builtin collections\n- [ ] `reactive(...)`: central `Rx*` construction for (builtin) types, functions, etc.\n- [ ] `Rx{File,Signal,Process,Socket,...}`: reactive IO (state) \n- [ ] [dataclasses](https://docs.python.org/3/library/dataclasses.html) integration\n- [ ] (optional) [python-attrs](https://github.com/python-attrs/attrs) integration\n- [ ] (optional) [pydantic](https://github.com/pydantic/pydantic) integration\n',
    'author': 'Joren Hammudoglu',
    'author_email': 'jhammudoglu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorenham/rxio',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
