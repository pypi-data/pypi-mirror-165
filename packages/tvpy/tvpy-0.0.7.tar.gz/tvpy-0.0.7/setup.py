# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvpy']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'fire>=0.4.0,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['tv-html = tvpy.main:tv_html',
                     'tv-json = tvpy.main:tv_json']}

setup_kwargs = {
    'name': 'tvpy',
    'version': '0.0.7',
    'description': '📺 TvPy',
    'long_description': '# 📺 TvPy \nGenerate html from folder names.\n\n## Installation\n```shell\n> pip install tvpy\n```\n\n## Get an API Key\nYou need to get an API key from [TMDB](https://www.themoviedb.org/settings/api) and save it as `key.txt` in your working directory.\n\n## Usage\n```shell\n> mkdir Carnival.Row Resident.Alien Liar Under.the.Banner.of.Heaven\n> tv-json . && tv-html\n```\n',
    'author': 'Gilad Kutiel',
    'author_email': 'gilad.kutiel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkutiel/tvpy/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
