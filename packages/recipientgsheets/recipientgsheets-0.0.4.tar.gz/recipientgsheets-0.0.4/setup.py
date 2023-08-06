# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['recipientgsheets']
setup_kwargs = {
    'name': 'recipientgsheets',
    'version': '0.0.4',
    'description': 'Модуль, который позволяет использовать данные из Google Таблицы, а также перевести её в csv файл',
    'long_description': "# ***Получение данных с Google таблиц***\n____\n### Установка\n```\npip install recipientgsheets\n```\n### Импорт и инициализация\n```python\nfrom recipientgsheets import RecipientGoogleSheets\n\ntableid = '1iVSut_5LLcXAeecJI73y0EmltL8mwg-9hEHaWP2UOp0'\nencoding = 'utf-8'\nsave_directory = 'table.csv'\n\ngttc = RecipientGoogleSheets(tableid,encoding,save_directory) # Инициализация класса\n```\n### Где найти tableid ?\n>Найти ID таблицы можно на том месте , где находится **ExampleID**                                     \n>https://docs.google.com/spreadsheets/d/ExampleID/edit#gid=0\n### Методы\n```python\ntocsv() # Делает из Гугл таблицы csv файл\n\nget_column(column_num) # Возвращает колонку таблицы по её номеру\n\nget_line(line_num) # Возвращает строку таблицы по её номеру\n\nget_cell(column_num,line_num) # Возвращает нужную ячейку в str\n```\n## Примечание\n>Важно чтобы таблица была открытой для общего доступа!\n## Полезные ссылки\n>[Страница на GitHub](https://github.com/DaniEruDai/recipientgsheets)\n\n\n\n",
    'author': 'DaniEruDai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
