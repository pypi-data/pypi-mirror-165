import cx_Oracle
import json


class Oracle:

    def __init__(self, host, port, sid, user, password, lib_dir=None, encoding='UTF-8'):
        self.__host = host
        self.__port = port
        self.__sid = sid
        self.__user = user
        self.__password = password
        self.__lib_dir = lib_dir
        self.__encoding = encoding

    def execute(self, *sql, array=True):
        if self.__lib_dir:
            cx_Oracle.init_oracle_client(lib_dir=self.__lib_dir)
            # https://www.oracle.com/database/technologies/instant-client.html
        with cx_Oracle.connect(
                user=self.__user,
                password=self.__password,
                dsn=cx_Oracle.makedsn(host=self.__host, port=self.__port, sid=self.__sid),
                encoding=self.__encoding) as connect:
            with connect.cursor() as cur:
                cur.execute(*sql)
                if cur.description:
                    cur.rowfactory = lambda *args: dict(zip([d[0] for d in cur.description], args))
                    result = cur.fetchall() if array else cur.fetchone()
                    return json.dumps(result, indent=4, default=str, ensure_ascii=False)
                else:
                    connect.commit()
                    return cur.rowcount
