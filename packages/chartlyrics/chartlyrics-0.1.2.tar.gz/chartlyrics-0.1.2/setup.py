# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chartlyrics']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'lxml>=4.9.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'chartlyrics',
    'version': '0.1.2',
    'description': 'Wrapper for chartlyrics api: http://api.chartlyrics.com',
    'long_description': '[![CircleCI Build Status](https://circleci.com/gh/matheusfillipe/chartlyrics.svg?style=shield)](https://circleci.com/gh/matheusfillipe/chartlyrics)\n[![Pypi](https://badge.fury.io/py/chartlyrics.svg)](https://pypi.org/project/chartlyrics/)\n[![Chat with me on irc](https://img.shields.io/badge/-IRC-gray?logo=gitter)](https://mangle.ga/irc)\n\n# ChartLyrics API\n\nThis is a simple wrapper for: http://api.chartlyrics.com. You can search for songs, artists and get the lyrics.\n\n## Installation\n\n``` sh\npip install chartlyrics\n```\n\n## Usage Example\n\n```python\nfrom chartlyrics import ChartLyricsClient\n\nclient = ChartLyricsClient()\n\nfor song in client.search_text("starts with one"):\n    if "park" in song.artist.lower():\n      print(song.artist)  # Linking Park\n      print(song.lyrics)  # Starts with one\\n One thing I dont know why...\n```\n\nYou can also use `song.lyrics_object` which will return a `Lyrics` object that you can index strophes and verses on:\n\n```python\nlyrics = song.lyrics_object\nprint(lyrics[0][-1])  # first strophe last verse\n```\n\nCheck the `tests` for more examples.\n\n## Development\n\nFork the repo, run:\n\n```sh\npoetry install\n```\n\nAdd features, write tests, run:\n\n```sh\npoetry run pytest\n```\n\nCreate a Pull request.\n',
    'author': 'matheusfillipe',
    'author_email': 'matheusfillipeag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/matheusfillipe/chartlyrics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
