# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyurbandict']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-urbandict',
    'version': '0.2.3',
    'description': 'Python wrapper for the Urban Dictionary API.',
    'long_description': '# python-urbandict\n\n[![version](https://img.shields.io/pypi/v/python-urbandict.svg)](https://github.com/Vitaman02/pyurbandict)\n[![versions](https://img.shields.io/pypi/pyversions/python-urbandict.svg)](https://github.com/Vitaman02/pyurbandict)\n[![Python package](https://github.com/Vitaman02/pyurbandict/actions/workflows/python-package.yml/badge.svg)](https://github.com/Vitaman02/pyurbandict/actions/workflows/python-package.yml)\n[![codecov](https://codecov.io/gh/Vitaman02/pyurbandict/branch/main/graph/badge.svg?token=A244XBTUVH)](https://codecov.io/gh/Vitaman02/pyurbandict)\n\nThis is a python project, that fetches definitions of words from urban dictionary\'s public API.\n\nFuture additions. PRs are always welcome :)\n* Calculate ratio of `thumbs_up` and `thumbs_down` and decide the probability of a correct definition.\n\n# Installation\n\n*Python 3.9 or higher is required*\n\nTo install the library you can use the following command:\n\n```\n# Linux/MacOS\npython3 -m pip install --upgrade python-urbandict\n\n# Windows\npy -3 -m pip install --upgrade python-urbandict\n```\n\nOr just try:\n\n```\npip install python-urbandict\n```\n\n# Quick Example\n\nYou can create an instance of the `UrbanDict` class and pass a word to it. After that you can use the `search` method that will retrieve the definitions from UrbanDictionary.\nIf you want to you can also leave the word attribute empty, in which case a random word is selected by UrbanDictionary.\n\n```python\nfrom pyurbandict import UrbanDict\n\nword = UrbanDict("python")\nresults = word.search()\nprint(results[0])\n\n>>> Definition(\n    word=\'python\',\n    definition=\'The best thing to happen to [Computer Science] students in a data and [file] structures or [algorithms] class.\',\n    example=\'Joe: "Man...I spent a week coding that [algorithm] in C."\\r\\nMoe: "I got it [done in one] evening with [Python]. It works great."\\r\\nJoe: "Say, what? Where can I download that?"\',\n    author=\'TheNextBillGates\',\n    thumbs_up=243,\n    thumbs_down=71,\n    sound_urls=[\'https://api.twilio.com/2008-08-01/Accounts/ACd09691b82112e4b26fce156d7c01d0ed/Recordings/RE7065a4ef810937cc16ae2b6e4b54b67d\'],\n    written_on=\'2010-03-24T05:24:18.000Z\',\n    permalink=\'http://python.urbanup.com/4826760\',\n    defid=4826760,\n    current_vote=\'\'\n)\n```\n\n# Links\n* [PyPi](https://pypi.org/project/python-urbandict/)\n',
    'author': 'Vitaman02',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vitaman02/pyurbandict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
