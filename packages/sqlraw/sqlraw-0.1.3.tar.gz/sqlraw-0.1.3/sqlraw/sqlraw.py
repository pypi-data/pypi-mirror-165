#!/usr/bin/env python

__author__ = "Uygun Bodur"
__copyright__ = "Copyright developer kitchen"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Uygun Bodur"
__email__ = "topluluk@developerkitchen.dev"
__status__ = "Production"
from typing import Optional, List
from sqlalchemy import text
import os
import redis


class SqlRaw:
    """

    CURRENT PATH SQL USE
    
    sql = SqlRaw().current()
    
    # Get sql File
    sql.load('example')  # example.sql 
    
    # Connect SQLAlchemy 
    sql.connect(conn)  # conn: SQLAlchemy engine.connect
    
    # Call Parameteres
    data = sql.fetchone({"id":101})  # data: dictionary object


    RAW SQL USE

    sql = SqlRaw.query("select * form product").connect(conn)
    list = sql.fetchall()  # list: List



    This library developed by developer::kitchen community is used to run and test the sql file.
    """

    def __init__(self, folders: Optional[List[str]] = ["."], 
            sql: Optional[str] = "") -> None:
        self.dirs = folders
        self.sql = sql
        self.connection = None
        self.isFolder = True  # Sql dosyasından okunacak
        self.isCache = False  # Redis entegrasyonu ile sorgular cache'e
        self.app_name = "sqlraw"
        self.r = None

    
    @classmethod
    def query(cls, sql: str):
        """
        Load raw query
        """
        _cls = cls(folders=[""], sql=sql)
        _cls.isFolder = False
        return _cls

    @classmethod
    def paths(cls, folders=["./model"]):
        """
        Paths to search for the SQL file. It also automatically searches subdirectories.
        Default value is "./model"
        """
        return cls(folders)

    @classmethod
    def current(cls):
        """
        SQL file is searched in current folder and subfolder
        """
        return cls()

    @property
    def cache_prefix(self):
        return self.app_name

    @cache_prefix.setter
    def cache_prefix(self, val):
        self.app_name = val

    def cache(self, host: str, port:Optional[int]=6379, 
            password: Optional[str] = ""):
        """
        Configure Cache System
        @host: Redis Url
        @username?: Redis user name
        @password?: Redis password
        """
        try:
            self.r = redis.Redis(host=host, port=port, db=0, password=password)
            self.isCache = True
            print("[OK] Redis is connected...")
        except:
            self.isCache = False
            print("[ERR]: Redis connection failed...")


        return self

    def clear_cache(self):
        if self.isCache and self.r is not None:
            key = f"{self.app_name}:*"
            for ki in self.r.keys(key):
                self.r.delete(ki)

    def _get_cache_key(self, key: str):
        key = key.lower().replace(".sql","")
        return f"{self.app_name}:{key}"

    def _set_cache(self, key: str, value: str):
        if not self.isCache or self.r is None:
            return
        key = self._get_cache_key(key)
        ret = self.r.set(key, value)
        print(f"[SET CACHE]:{ret}")

    def _get_cache(self, key):
        if not self.isCache or self.r is None:
            return None

        key = self._get_cache_key(key)
        ret = self.r.get(key)
        return ret.decode("utf-8") if ret is not None else None


    def _read_file(self, file_name: str, path: str):
        with open(f"{path}/{file_name}", encoding="utf8") as sql_file:
            self.sql = sql_file.read()
            self._set_cache(file_name, self.sql)

    def load(self, file_name: str):
        """
        The file is searched in the path and subfolders specified with "env". 
        The first found SQL file is read. 

        The file extension must be .sql
        @file_name can also be used without .sql extension
        """
        print(f"isCache: {self.isCache}")
        if self.isCache:
            cache_return = self._get_cache(file_name)
            print(f"[Cache Return]: {cache_return is not None}")
            if cache_return is not None:
                self.sql = cache_return
                return self

        if ".sql" not in file_name:
            file_name = f"{file_name}.sql"


        for dir in self.dirs:
            for root, _, files in os.walk(dir):
                for file in files:
                    if file == file_name:
                        self._read_file(file_name, root)
                        return self

        return self

    def connect(self, conn):
        """
        @conn is SQLAlchemy connection object
        """
        self.connection = conn
        return self

    def _convert_tolist(self, result_set):
        return [dict(r) for r in result_set]

    def execute(self, params=None):
        """
        Execure Query for insert & update
        @params? : Dictionary parameters object

        """
        try:
            self.connection.execute(text(self.sql), params if params else {})
            return True
        except Exception as e:
            print(e)
            raise Exception(e)

    def fetchall(self, params=None):
        """
        Fetch all data
        @params? : Dictionary parameters object
        """
        try:
            return_set = self.connection.execute(text(self.sql), params if params else {})
            return self._convert_tolist(return_set)
        except Exception as e:
            print(e)
            raise Exception(e)

    def fetchone(self, params=None):
        try:
            return_set = self.connection.execute(text(self.sql), params if params else {})
            return_set = self._convert_tolist(return_set)
            return return_set[0] if len(return_set) > 0 else None
        except Exception as e:
            raise Exception(e)
 
