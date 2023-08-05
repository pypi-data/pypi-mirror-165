# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyccup']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0', 'hy==0.24.0', 'hyrule', 'toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'hyccup',
    'version': '1.0.0',
    'description': 'A port of Clojure Hiccup for Hy',
    'long_description': '# Hyccup\n\n[![PyPi](https://img.shields.io/pypi/v/hyccup?label=PyPi)](https://pypi.org/project/hyccup/)\n[![Python Version](https://img.shields.io/pypi/pyversions/hyccup?label=Python)](https://pypi.org/project/hyccup/)\n[![CI](https://github.com/Arkelis/hyccup/actions/workflows/ci.yml/badge.svg)](https://github.com/Arkelis/hyccup/actions/workflows/ci.yml)\n[![CD](https://github.com/Arkelis/hyccup/actions/workflows/cd.yml/badge.svg)](https://github.com/Arkelis/hyccup/actions/workflows/cd.yml)\n\nHyccup is a port of [Hiccup](https://github.com/weavejester/hiccup)\nfor [Hy](https://github.com/hylang/hy), a Lisp embed in Python.\n\nIt allows you to represent HTML into data structure and to dump it.\n\n```hy\n=> (import hyccup.core [html])\n=> (html [\'div {\'class "my-class" \'id "my-id"} "Hello Hyccup"])\n"<div class=\\"my-class\\" id=\\"my-id\\">Hello Hyccup</div>"\n```\n\nHyccup can also be used in Python:\n\n```pycon\n>>> from hyccup.core import html\n>>> html([\'div\', {\'class\': \'my-class\', \'id\': \'my-id\'}, \'Hello Hyccup\'])\n\'<div class="my-class" id="my-id">Hello Hyccup</div>\'\n```\n\nMore information in the [documentation](https://hyccup.pycolore.fr).\n',
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arkelis/hyccup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
