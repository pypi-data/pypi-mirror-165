# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genius', 'genius.classes']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'wrap-genius',
    'version': '1.7.1',
    'description': 'Python wrapper for api.genius.com',
    'long_description': ' # wrap-genius\n\n[![Version](https://img.shields.io/pypi/v/wrap-genius?logo=pypi)](https://pypi.org/project/wrap-genius)\n[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)\n[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)\n\nPython wrapper for genius.com\'s API\n\n\n## Setup\n\n**wrap-genius** is supported on Python 3.8+ and it can be installed using [pip](https://pypi.python.org/pypi/pip).\n\n```bash\npip install wrap-genius\n```   \n\nTo be able to use it, you\'ll need to create an API client for [genius.com](https://genius.com/api-clients) and get a **CLIENT ACCESS TOKEN**.\n\n\n## Quickstart\n\nAssuming you already have you access token, get an instance of the genius wrapper as follows:\n\n```python\nfrom genius import Genius\ng = Genius(access_token="YOUR-TOKEN")\n```   \n\nWith this instance you can interact with genius in many ways:\n\n```python\n# Search for an artist by name\nartist = g.search_artist("Gorillaz")\nprint(artist)\n```\n```text\n>> "Gorillaz (860)"\n```\n\n\n```python\n# Get the artist\'s song by popularity\nfor song in artist.songs_by_popularity:\n    print(song)\n```\n```text\n>> "Feel Good Inc. (21569)"\n>> "Clint Eastwood (1698)"\n>> "Saturnz Barz (3027437)"\n>> "Ascension (3027418)"\n>> "On Melancholy Hill (53533)"\n>> ...\n```\n\n\n```python\n# Get the details of a song by its id\nsong = g.get_song(song_id=3027414)\nprint(song.title_with_featured)\nprint(song.release_date_for_display)\n```\n```text\n>> "Andromeda (Ft. DRAM)"\n>> "March 23, 2017"\n```\n\n\n```python\n# Get the song album, or the featured artists\nprint(song.album)\nfor featured in song.features:\n    print(featured.name)\n```\n```text\n>> "Humanz (335930)"\n>> "DRAM (241761)"\n```\n\n```python\n# And even, a song\'s lyrics\nlyrics = song.lyrics\nprint(\'\\n\'.join(lyrics))\n```\n```text\n>> "[Verse 1: 2-D]"\n>> "When the pulsing looks to die for"\n>> "Take it in your heart now, lover"\n>> "When the case is out"\n>> "And tired and sodden"\n>> "Take it in your heart"\n>> "Take it in your heart"\n>> ...\n```',
    'author': 'Fede Calendino',
    'author_email': 'fede@calendino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedecalendino/wrap-genius',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
