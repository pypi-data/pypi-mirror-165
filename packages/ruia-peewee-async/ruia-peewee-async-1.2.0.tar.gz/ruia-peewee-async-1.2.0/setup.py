# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruia_peewee_async']

package_data = \
{'': ['*']}

install_requires = \
['peewee-async>=0.8.0,<0.9.0', 'ruia>=0.8.4,<0.9.0']

extras_require = \
{'aiomysql': ['aiomysql>=0.1.1,<0.2.0'],
 'aiopg': ['aiopg>=1.3.4,<2.0.0'],
 'all': ['aiomysql>=0.1.1,<0.2.0', 'aiopg>=1.3.4,<2.0.0']}

setup_kwargs = {
    'name': 'ruia-peewee-async',
    'version': '1.2.0',
    'description': 'A Ruia plugin that uses the peewee-async to store data to MySQL',
    'long_description': '# ruia-peewee-async\n[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)\n[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)\n\nA [Ruia](https://github.com/howie6879/ruia) plugin that uses [peewee-async](https://github.com/05bit/peewee-async) to store data to MySQL or PostgreSQL or both of them.\n\n\n## Installation\n\n```shell\npip install ruia-peewee-async[aiomysql]\n\nor\n\npip install ruia-peewee-async[aiopg]\n\nor\n\npip install ruia-peewee-async[all]\n```\n\n## Usage\n\n\n```python\nfrom peewee import CharField\nfrom ruia import AttrField, Item, Response, Spider, TextField\n\nfrom ruia_peewee_async import (RuiaPeeweeInsert, RuiaPeeweeUpdate, TargetDB,\n                               after_start)\n\nclass DoubanItem(Item):\n    target_item = TextField(css_select="tr.item")\n    title = AttrField(css_select="a.nbg", attr="title")\n    url = AttrField(css_select="a.nbg", attr="href")\n\n    async def clean_title(self, value):\n        return value.strip()\n\nclass DoubanSpider(Spider):\n    start_urls = ["https://movie.douban.com/chart"]\n    # aiohttp_kwargs = {"proxy": "http://127.0.0.1:7890"}\n\n    async def parse(self, response: Response):\n        async for item in DoubanItem.get_items(html=await response.text()):\n            yield RuiaPeeweeInsert(item.results)  # default is MySQL\n            # yield RuiaPeeweeInsert(item.results, database=TargetDB.POSTGRES) # save to Postgresql\n            # yield RuiaPeeweeInsert(item.results, database=TargetDB.BOTH) # save to both MySQL and Postgresql\n\nclass DoubanUpdateSpider(Spider):\n    start_urls = ["https://movie.douban.com/chart"]\n\n    async def parse(self, response: Response):\n        async for item in DoubanItem.get_items(html=await response.text()):\n            res = {}\n            res["title"] = item.results["title"]\n            res["url"] = "http://whatever.youwanttoupdate.com"\n            yield RuiaPeeweeUpdate(\n                res,\n                {"title": res["title"]},\n                database=TargetDB.POSTGRES,  # default is MySQL\n            )\n\n            # Args for RuiaPeeweeUpdate\n            # data: A dict that\'s going to be updated in the database.\n            # query: A peewee query or a dict to search for the target data in database.\n            # database: The target database type.\n            # create_when_not_exists: If True, will create a record when data not exists. Default is True.\n            # only: A list or tuple of fields that should be updated.\n\nmysql = {\n    "host": "127.0.0.1",\n    "port": 3306,\n    "user": "ruiamysql",\n    "password": "abc123",\n    "database": "ruiamysql",\n    "model": {\n        "table_name": "ruia_mysql",\n        "title": CharField(),\n        "url": CharField(),\n    },\n}\npostgres = {\n    "host": "127.0.0.1",\n    "port": 5432,\n    "user": "ruiapostgres",\n    "password": "abc123",\n    "database": "ruiapostgres",\n    "model": {\n        "table_name": "ruia_postgres",\n        "title": CharField(),\n        "url": CharField(),\n    },\n}\n\nif __name__ == "__main__":\n    DoubanSpider.start(after_start=after_start(mysql=mysql))\n    # DoubanSpider.start(after_start=after_start(postgres=postgres))\n    # DoubanSpider.start(after_start=after_start(mysql=mysql, postgres=postgres))\n    # DoubanUpdateSpider.start(after_start=after_start(mysql=mysql))\n```\n\n## Development\nUsing `pyenv` to install the version of python that you need.\nFor example\n```shell\npyenv install 3.7.15\n```\nThen go to the root of the project and run:\n```shell\npoetry install\n```\nto install all dependencies.\n\nUsing `poetry shell` to enter the virtual environment. Or open your favorite editor and select the virtual environment to start coding.\n\nUsing `pytest` to run unit tests under `tests` folder.\n',
    'author': 'Jack Deng',
    'author_email': 'dlwxxxdlw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JackTheMico/ruia-peewee-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
