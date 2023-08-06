from mysql.connector import connect
from contextlib import closing
import json


class MySQL:

    def __init__(self, host, port, database, user, password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

    def execute(self, *sql, array=True):
        with closing(connect(database=self.__database,
                             user=self.__user,
                             password=self.__password,
                             host=self.__host,
                             port=self.__port)) as connection:
            with connection.cursor(dictionary=True) as cur:
                cur.execute(*sql)
                if cur.description:
                    result = cur.fetchall() if array else cur.fetchone()
                    return json.dumps(result, indent=4, default=str, ensure_ascii=False)
                else:
                    connection.commit()
                    return cur.rowcount
