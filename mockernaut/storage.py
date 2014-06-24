
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


class MySQLStorage(object):
    DoesNotExists = DoesNotExists

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_by_id(self, _id):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules WHERE id=%s", (_id,))

        data = cursor.fetchone()

        cursor.close()
        con.close()

        return self.make_rule(data)

    def get_all(self):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules")

        data = cursor.fetchall()

        cursor.close()
        con.close()

        return [self.make_rule(item) for item in data]

    def get_by_path(self, path):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules WHERE path=%s", (path,))

        data = cursor.fetchone()

        cursor.close()
        con.close()

        return self.make_rule(data)

    def make_rule(self, data):
        if not data:
            raise DoesNotExists

        path = data.pop('path')
        data['request'] = loads(data['request'])

        data['response'] = loads(data['response'])

        return data

    def add(self, item):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        sql = 'INSERT INTO `rules` (`path`, `request`, `response`)' \
              'VALUES (%s, %s, %s)'

        cursor.execute(sql, (
            item['request']['path'],
            dumps(item['request']),
            dumps(item['response'])
        ))

        item['id'] = cursor.lastrowid

        con.commit()
        cursor.close()
        con.close()

        return item

    def delete_by_id(self, _id):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("DELETE FROM rules WHERE id=%s", (_id,))
        con.commit()

        cursor.close()
        con.close()

        if cursor.rowcount == 0:
            raise DoesNotExists

    def get_by_request(self, request):
        raise NotImplementedError

    def delete_all(self):
        con = self.pool.get_connection()
        cursor = con.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("DELETE FROM rules")
        con.commit()

        cursor.close()
        con.close()

    def get_by_request(self, request):
        raise NotImplementedError


storage_class = MySQLStorage
