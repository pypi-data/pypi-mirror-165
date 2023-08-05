# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oppapi']

package_data = \
{'': ['*']}

install_requires = \
['okome>=0.0.1,<0.0.2', 'pyserde>=0.9.0']

setup_kwargs = {
    'name': 'oppapi',
    'version': '0.0.5',
    'description': '',
    'long_description': '# `oppapī`\n\n*Ergonomic option parser on top of [dataclasses](https://docs.python.org/3/library/dataclasses.html), inspired by [structopt](https://github.com/TeXitoi/structopt).*\n\n<p align="center">\n  <img src="logo.png" width=25% />\n</p>\n\n## Usage\n\n```python\nfrom typing import Optional\nfrom oppapi import from_args, oppapi\n\n@oppapi\nclass Opt:\n    """\n    Option parser using oppapi\n    """\n\n    host: str\n    """ This will be positional argument of type `str` """\n\n    port: Optional[int] = 8000\n    """ Optional argument will be option argument """\n\nopt = from_args(Opt)\nprint(opt)\n```\n\nThe code above generates such option parser that\n* Generates parser description from class\'s docstring\n* Generates argument description from field\'s docstring\n* A field will be a positional argument\n* An optional field will be an optional argument\n\nSee the parser help message:\n\n```\n$ python simple.py -h\nusage: simple.py [-h] [-p PORT] host\n\nOption parser using oppapi\n\npositional arguments:\n  host                  This will be positional argument of type `str`\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PORT, --port PORT  Optional argument will be option argument\n```\n\nRunning the program deserializes the command line arguments into an object of the declared class.\n\n```\n$ python simple.py localhost -p 20000\nOpt(host=\'localhost\', port=20000)\n```\n\n## Supported types\n\n* Primitives (`int`, `float`, `str`, `bool`)\n* Containers (`List`, `Tuple`)\n* [`typing.Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)\n* [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) and [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum)\n* [`datetime`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_datetime.py)\n* [`decimal`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_decimal.py)\n* [`ipaddress`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_ipaddress.py)\n* [`pathlib`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_path.py)\n* [`uuid`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_uuid.py)\n\n\n## `short`/`long`\n\n`oppapi` generates flag names automatically, but you can specify arbitrary short/long names.\n\n```python\nfrom typing import Optional\nfrom oppapi import from_args, oppapi, field\n\n@oppapi\nclass Opt:\n    host: Optional[str] = field(short="-n", long="--hostname")\n```\n\n## `enum`\n\n`enum.Enum` and `enum.IntEnum` will be an argument with [choices](https://docs.python.org/3/library/argparse.html#choices) parameter.\n\n```python\nclass Food(Enum):\n    A = "Apple"\n    B = "Beer"\n    C = "Chocolate"\n\nclass Price(IntEnum):\n    A = 10\n    B = 20\n    C = 30\n\n@oppapi\nclass Opt:\n    food: Food\n    price: Optional[Price]\n```\n\nusage will be like this:\n```\npositional arguments:\n  {Apple,Beer,Chocolate}\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p {10,20,30}, --price {10,20,30}\n```\n\noppapi converts the command line arguments back to Enum.\n\n```python\n$ python choice.py Apple --price 20\nOpt(food=<Food.A: \'Apple\'>, price=<Price.B: 20>)\n```\n\n## `List`/`Tuple`\n\n`List` will be an arbitrary number of arguments (`nargs="+"`). `Tuple` will be a fixed number of arguments (`nargs=NUM`).\n\n```python\n@oppapi\nclass Opt:\n    values: List[int]\n    opts: Optional[Tuple[int, str, float, bool]]\n```\n\n```\n$ python nargs.py 1 2 3 --opts 10 foo 10.0 True\nOpt(values=[1, 2, 3], opts=(10, \'foo\', 10.0, True))\n```\n\n## SubCommand\n\n`Union` of dataclasses will be subcommands.\n\n```python\n@oppapi\nclass Foo:\n    a: int\n\n@oppapi\nclass Bar:\n    a: str\n    b: Optional[int]\n\n@oppapi\nclass Opt:\n    sub: Union[Foo, Bar]\n\n```\n\n```\nusage: subcommand.py [-h] {foo,bar} ...\n\npositional arguments:\n  {foo,bar}\n\n  optional arguments:\n    -h, --help  show this help message and exit\n```\n\n## Flatten\n\nTODO\n\n## LICENSE\n\nThis project is licensed under the [MIT license](https://github.com/yukinarit/oppapi/blob/main/LICENSE)\n',
    'author': 'yukinarit',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yukinarit/oppapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
