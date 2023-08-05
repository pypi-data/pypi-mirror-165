# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['videocdn_tv',
 'videocdn_tv.models',
 'videocdn_tv.models.api',
 'videocdn_tv.models.contents',
 'videocdn_tv.models.episodes',
 'videocdn_tv.models.seasons',
 'videocdn_tv.params',
 'videocdn_tv.type']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0', 'requests==2.26.0']

setup_kwargs = {
    'name': 'videocdn-tv',
    'version': '0.1.8',
    'description': 'Реализация Api для сервиса VideoCDN.tv',
    'long_description': '# VideoCND - API\n\nРеализация Api для сервиса VideoCDN.tv\n\nУстановка:```pip install videocdn-tv```\n\n## Методы\n\nВзаимодействие:\n\n```python\nfrom .videocdn import VideoCDN, ParamsContent, ParamsEpisode, ParamsSeason\nvideocdn = VideoCDN(api_token="KEY")\n```\n\n### translations\n\n```python\ndata = videocdn.get_translations()\n```\n\n### movies\n\n```python\ndata = videocdn.get_movies(ParamsContent(query="Аквамене"))\n```\n\n### animes\n\n```python\ndata = videocdn.get_animes(ParamsContent(query="Ван-Пис: Золото"))\n```\n\n### tv-series\n\n```python\ndata = videocdn.get_tv_series(ParamsContent(query="Игра Пристолов"))\n```\n\n### tv-series/seasons\n\n```python\ndata = videocdn.get_tv_series_seasons(ParamsSeason(tv_series_id=1))\n```\n\n### tv-series/episodes\n\n```python\ndata = videocdn.get_tv_series_episodes(ParamsEpisode(tv_series_id=1))\n```\n\n### anime-tv-series\n\n```python\ndata = videocdn.get_anime_tv_series(ParamsContent(query="Доктор Стоун"))\n```\n\n### anime-tv-series/seasons\n\n```python\ndata = videocdn.get_anime_tv_series_seasons(ParamsSeason(tv_series_id=1))\n```\n\n### anime-tv-series/episodes\n\n```python\ndata = videocdn.get_anime_tv_series_episodes(ParamsEpisode(tv_series_id=1))\n```\n\n### show-tv-series\n\n```python\ndata = videocdn.get_show_tv_series(ParamsContent(query="Зовите шефа"))\n```\n\n### show-tv-series/seasons\n\n```python\ndata = videocdn.get_show_tv_series_season(ParamsSeason(tv_series_id=1))\n```\n\n### show-tv-series/episodes\n\n```python\ndata = videocdn.get_show_tv_series_episodes(ParamsEpisode(tv_series_id=1))\n```',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/odi1n/VideoCDN',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
