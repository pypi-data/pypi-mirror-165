# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyonize']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyonize',
    'version': '0.1.5',
    'description': 'convert json|dict to python object',
    'long_description': '# Pyonize\n\nconvert json|dict to python object\n\n## Setup\n\n```\npip install pyonize\n```\n\n## Examples\n```py\nfrom pyonize import pyonize\n\ndeneme = pyonize({"id": 1, "name": "jhon", "job": {"id": 1, "title": "CTO"}, "list": [\n                1, 2, 3], "dictlist": [{"name": "foo"}, {"name": "bar"}]})\n\nprint(deneme.name)\nprint(deneme.job)\nprint(deneme.job.title)\n```\n\n##\n\n```py\nfrom pyonize import Pyon\n\nclass Foo(Pyon):\n    def bar(self):\n        ...\n\ndata = {"id": 1, "name": "jhon", "job": {"id": 1, "title": "CTO"},\n    "list": [1, 2, 3], "dictlist": [{"name": "foo"}, {"name": "bar"}]}\n\nfoo = Foo(data)\n\nprint(foo.id)\nprint(foo.dictlist[1].name)\n\n```\n\n<br>\n<hr>\n\n',
    'author': 'Bilal Alpaslan',
    'author_email': 'm.bilal.alpaslan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BilalAlpaslan/Pyonize',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
