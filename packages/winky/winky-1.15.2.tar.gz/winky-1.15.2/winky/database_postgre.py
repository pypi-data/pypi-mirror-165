from psycopg2.extras import RealDictCursor
from contextlib import closing
import psycopg2.errors
import psycopg2
import json


class Postgre:

    def __init__(self, host, port, database, user, password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

    def execute(self, *sql, array=True):
        with closing(psycopg2.connect(dbname=self.__database,
                                      user=self.__user,
                                      password=self.__password,
                                      host=self.__host,
                                      port=self.__port)) as connect:
            with connect.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(*sql)
                if cur.description:
                    result = cur.fetchall() if array else cur.fetchone()
                    return json.dumps(result, indent=4, default=str, ensure_ascii=False)
                else:
                    connect.commit()
                    return cur.rowcount
