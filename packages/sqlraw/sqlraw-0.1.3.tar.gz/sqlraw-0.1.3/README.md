
# SQLRaw

SQLRaw is a library that makes it easy to run .sql files that work with a SQLAlchemy.

## First of all, SQLAlchemy connection definition are made

``` python
connstr = "postgresql://user:psw@host/database"
engine = create_engine(connstr, echo=False)
conn = engine.connect()
```

## Read & Execute Current Sub Folders SQL File

``` python
sql = SqlRaw.current()
sql.load("person").connect(conn)
list = sql.fetchone({"id": 1})
```

In this example, the file "person.sql" is searched and executed in the current
folder or subfolders. If there is a parameter definition such as ":id" in SQL,
a value can be assigned to the "fetchone" method as a parameter.

**Also Note that "fetchone" can be used instead of "fetchall"**

## Reading a file in a specific folder

```python
sql = SqlRaw.paths(["/model"])
```

## Use Cache

```python
sql.cache_prefix = "app-name-prefix"
sql.cache(host='', port=6379, password='')
```

