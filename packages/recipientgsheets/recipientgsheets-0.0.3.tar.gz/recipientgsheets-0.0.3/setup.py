# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['recipientgsheets']
setup_kwargs = {
    'name': 'recipientgsheets',
    'version': '0.0.3',
    'description': 'Модуль, который позволяет использовать данные из Google Таблицы, а также перевести её в csv файл',
    'long_description': "# ***Гугл таблицы в csv файл***\n> **Преобразует гугл таблицу по ссылке и сохраняет в csv файл**\n## Установка | install\n```\npip install googletabletocsv\n```\n## Пример\n### Импорт и инициализация\n```python\nfrom googletabletocsv import GtableToCsv\n\ntableid = '1iVSut_5LLcXAeecJI73y0EmltL8mwg-9hEHaWP2UOp0'\nencoding = 'utf-8'\nsave_directory = 'table.csv'\n\ngttc = GtableToCsv(tableid,encoding,save_directory) # Инициализация класса\n```\n### Методы\n```python\nget_column(column_num) # Возвращает колонку таблицы по её номеру\n\nget_line(line_num) # Возвращает строку таблицы по её номеру\n\nalltocsv() # Делает из Гугл таблицы csv файл\n```\n\n## Где найти tableid ?\n>Найти ID таблицы можно на том месте , где находится **рука**                                     \n>https://docs.google.com/spreadsheets/d/:wave:/edit#gid=0\n\n## Примечание\n>Важно чтобы таблица была открытой для общего доступа!\n\n## Полезные ссылки\n>[Страница на PyPi](https://pypi.org/project/googletabletocsv)\n\n\n\n",
    'author': 'DaniEruDai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
