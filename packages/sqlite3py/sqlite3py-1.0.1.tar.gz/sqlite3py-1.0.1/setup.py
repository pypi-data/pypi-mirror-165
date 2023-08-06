from io import open
from setuptools import setup

version = '1.0.1'

with open('./README.md', encoding = 'utf-8') as readme:
    long_description = readme.read()

setup(
    name = 'sqlite3py',
    version = version,

    author = 'Xpos587',
    author_email = 'x30827pos@gmail.com',

    description = (
        'Module sqlite3py provides you smart requests for sqlite database',
        'By Xpos587'
    ),

    long_description = long_description,
    long_description_content_type = 'text/markdown',

    url = 'https://github.com/Xpos587/Sqlite3py',
    download_url = f'https://github.com/Xpos587/Sqlite3py/releases/v{version}.zip',

    license = 'MIT License, Copyright (c) 2022 Xpos587, see LICENSE file.',
    packages = ['sqlite3py'],

    requires = ['sqlite3']
)