# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shiki4py', 'shiki4py.store']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pyrate-limiter>=2.8.1,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'shiki4py',
    'version': '2.0.1',
    'description': 'Asynchronous client for api Shikimori written in Python 3.7 with asyncio and aiohttp.',
    'long_description': '# Shiki4py\n[![PyPi Package Version](https://img.shields.io/pypi/v/shiki4py?color=blue)](https://pypi.org/project/shiki4py)\n[![Supported python versions](https://img.shields.io/pypi/pyversions/shiki4py.svg)](https://pypi.org/project/shiki4py)\n\nАсинхронный клиент для взаимодействия с [api Shikimori](https://shikimori.one/api/doc/1.0), написанный на Python 3.7 c использованием [asyncio](https://docs.python.org/3/library/asyncio.html) и [aiohttp](https://github.com/aio-libs/aiohttp).\n\nВерсии shiki4py v0.2.2 и раньше являются синхронными, но начиная с v2.0.0 этот пакет стал асинхронным. Рекомендую использовать в своих проектах только shiki4py >= v2.0.0!\n\nСравнение shiki4py v0.2.2 и v2.0.0 по времени отправки 25 запросов:\n\n<img alt="Shiki4py sync vs async" src="https://raw.githubusercontent.com/ren3104/Shiki4py/main/assets/sync_vs_async.svg" width="500">\n\nshiki4py v0.2.2 ~10.5 секунд\n<details>\n<summary>Код</summary>\n\n```python\nfrom shiki4py import Client\n\n\nclient = Client("APP_NAME",\n                "CLIENT_ID",\n                "CLIENT_SECRET")\nfor i in range(25):\n    client.get(f"/users/{i}/info")\n```\n</details>\n\nshiki4py v2.0.0 ~5.07 секунд\n<details>\n<summary>Код</summary>\n\n```python\nfrom shiki4py import Shikimori\nimport asyncio\n\n\nasync def main():\n    async with Shikimori("APP_NAME", "CLIENT_ID", "CLIENT_SECRET") as api:\n        await asyncio.gather(*[api.request(f"/api/users/{i}/info") for i in range(25)])\n\n\nasyncio.run(main())\n```\n</details>\n\n## Особенности\n* Поддержка api v1 и v2\n* Ограничения 5rps и 90rpm\n* OAuth2 авторизация\n* Контроль срока действия токена\n* Хранение токенов в .env файле\n* Функция безопасного создания комментариев\n\n## Установка\n```bash\npip install shiki4py\n```\n\n## Использование\n### Быстрый старт\n```python\nfrom shiki4py import Shikimori\nimport asyncio\nimport logging\n\n\nlogging.basicConfig(level=logging.INFO)\n\n\nasync def main():\n    # Клиент без авторизации\n    async with Shikimori("APP_NAME") as api:\n        clubs = await api.request("/api/clubs", params={\n            "search": "Детектив Конан"\n        })\n        print(clubs)\n\n    # Клиент с авторизацией\n    api = Shikimori(\'APP_NAME\',\n                    \'CLIENT_ID\',\n                    \'CLIENT_SECRET\')\n    await api.open()\n    # Отправляем запросы\n    # await api.request(...)\n    # ...\n    await api.close()\n\n\nasyncio.run(main())\n```\n### Сохранение токенов авторизации\nПо умолчанию клиент сохраняет токены авторизации в файле .env, но при инициализации можно выбрать другой вариант хранения токенов, либо создать свой вариант унаследовав базовый класс и переопределив его методы.\n```python\nfrom shiki4py import Shikimori\nfrom shiki4py.store import BaseTokenStore\nfrom shiki4py.store.memory import MemoryTokenStore\n\n\nclass MyTokenStore(BaseTokenStore):\n    ...\n\n\napi = Shikimori(\'APP_NAME\',\n                \'CLIENT_ID\',\n                \'CLIENT_SECRET\',\n                # store=MyTokenStore()\n                store=MemoryTokenStore())\nawait api.open()\n```\n\n## Зависимости\n* [aiohttp](https://github.com/aio-libs/aiohttp) - для асинхронных HTTP запросов\n* [PyrateLimiter](https://github.com/vutran1710/PyrateLimiter) - для ограничения частоты запросов\n* [python-dotenv](https://github.com/theskumar/python-dotenv) - для сохранения токенов авторизации в `.env` файл\n',
    'author': 'ren3104',
    'author_email': '2ren3104@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ren3104/Shiki4py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
