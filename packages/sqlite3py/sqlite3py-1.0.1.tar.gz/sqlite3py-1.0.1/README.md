sqlite3py
=========

Module sqlite3py provides you smart requests for sqlite database.

Requirements Packages
---------------------
- sqlite3 (Already set by default)

#### **Example**

```python
from sqlite3py import Database

database = Database()

database.createTable('people', 'name TEXT NOT NULL, age INTEGER NOT NULL')

database.insert('people', 'name, age', '"Jhon", 24')

print(*database.get('people', '*'))
```

#### **Example**

```python
from sqlite3py import Database

database = Database()

database.createTable('people', 'name TEXT NOT NULL, age INTEGER NOT NULL')

database.insert('people', 'name, age', '"Jhon", 24')
database.insert('people', 'name, age', '"Michail", 19')

print(*database.get('people', '*'))

database.set('people', 'age = 20', 'WHERE name = "Michail"')

print(*database.get('people', '*'))

database.delete('people', 'WHERE name = "Jhon"')

print(*database.get('people', '*'))
```