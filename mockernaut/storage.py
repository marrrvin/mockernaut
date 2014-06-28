
from json import dumps
from json import loads

from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import cursor

from .errors import DoesNotExists


class MySQLCursorDict(cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))

        return None


class SafeMySQLConnectionPool(object):
    def __init__(self, pool):
        self.pool = pool
        self.con = None

    def __enter__(self):
        self.con = self.pool.get_connection()

        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()


def _make_rule(data):
    if not data:
        raise DoesNotExists('Rule does not exists.')

    data.pop('path')
    data['request'] = loads(data['request'])
    data['response'] = loads(data['response'])

    return data


class MySQLStorage(object):
    DoesNotExists = DoesNotExists

    def __init__(self, **kwargs):
        self.pool = SafeMySQLConnectionPool(MySQLConnectionPool(**kwargs))

    def get_by_path(self, path):
        with self.pool as con:
            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules WHERE path=%s", (path,))

            data = cur.fetchone()

            return _make_rule(data)

    def get_by_id(self, _id):
        with self.pool as con:
            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules WHERE id=%s", (_id,))

            data = cur.fetchone()

            return _make_rule(data)

    def get_list(self):
        with self.pool as con:
            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules")

            data = cur.fetchall()

            return [_make_rule(item) for item in data]

    def create(self, item):
        sql = 'INSERT INTO `rules` (`path`, `request`, `response`)' \
              'VALUES (%s, %s, %s)'

        with self.pool as con:
            cur = con.cursor(cursor_class=MySQLCursorDict)

            cur.execute(sql, (
                item['request']['path'],
                dumps(item['request']),
                dumps(item['response'])
            ))
            item['id'] = cur.lastrowid

            con.commit()

        return item

    def delete_by_id(self, _id):
        with self.pool as con:
            cur = con.cursor()
            cur.execute("DELETE FROM rules WHERE id=%s", (_id,))
            con.commit()

            if cur.rowcount == 0:
                raise DoesNotExists('Rule with id={id} does not exists.'.format(id=_id))

    def clear(self):
        with self.pool as con:
            cur = con.cursor()
            cur.execute('TRUNCATE TABLE `rules`')
            con.commit()


storage_class = MySQLStorage
