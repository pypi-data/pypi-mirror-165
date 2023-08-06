# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlraw']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0', 'psycopg2>=2.9.3,<3.0.0', 'redis>=4.2.2,<5.0.0']

setup_kwargs = {
    'name': 'sqlraw',
    'version': '0.1.3',
    'description': 'Path base SQL Query',
    'long_description': '\n# SQLRaw\n\nSQLRaw is a library that makes it easy to run .sql files that work with a SQLAlchemy.\n\n## First of all, SQLAlchemy connection definition are made\n\n``` python\nconnstr = "postgresql://user:psw@host/database"\nengine = create_engine(connstr, echo=False)\nconn = engine.connect()\n```\n\n## Read & Execute Current Sub Folders SQL File\n\n``` python\nsql = SqlRaw.current()\nsql.load("person").connect(conn)\nlist = sql.fetchone({"id": 1})\n```\n\nIn this example, the file "person.sql" is searched and executed in the current\nfolder or subfolders. If there is a parameter definition such as ":id" in SQL,\na value can be assigned to the "fetchone" method as a parameter.\n\n**Also Note that "fetchone" can be used instead of "fetchall"**\n\n## Reading a file in a specific folder\n\n```python\nsql = SqlRaw.paths(["/model"])\n```\n\n## Use Cache\n\n```python\nsql.cache_prefix = "app-name-prefix"\nsql.cache(host=\'\', port=6379, password=\'\')\n```\n\n',
    'author': 'Uygun Bodur',
    'author_email': 'uygun@dop.com.tr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/developerkitchentr/sqlraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
