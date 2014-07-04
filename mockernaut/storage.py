
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


def _make_rule(data):
    data.pop('path')
    data['request'] = loads(data['request'])
    data['response'] = loads(data['response'])

    return data


class MySQLStorage(object):
    DoesNotExists = DoesNotExists

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_by_path(self, path):
        con = None
        cur = None
        try:
            con = self.pool.get_connection()

            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules WHERE path=%s", (path,))

            data = cur.fetchall()

            return [_make_rule(item) for item in data]
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def get_by_id(self, _id):
        con = None
        cur = None
        try:
            con = self.pool.get_connection()
            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules WHERE id=%s", (_id,))

            data = cur.fetchone()
            if not data:
                raise DoesNotExists('Rule does not exists.')

            return _make_rule(data)
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def get_list(self):
        con = None
        cur = None
        try:
            con = self.pool.get_connection()
            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute("SELECT * FROM rules")

            data = cur.fetchall()

            return [_make_rule(item) for item in data]
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def create(self, item):
        sql = 'INSERT INTO `rules` (`path`, `request`, `response`)' \
              'VALUES (%s, %s, %s)'

        con = None
        cur = None
        try:
            con = self.pool.get_connection()
            cur = con.cursor(cursor_class=MySQLCursorDict)

            cur.execute(sql, (
                item['request']['path'],
                dumps(item['request']),
                dumps(item['response'])
            ))
            item['id'] = cur.lastrowid

            con.commit()

            return item
        except:
            if con is not None:
                con.rollback()
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def delete_by_id(self, _id):
        con = None
        cur = None
        try:
            con = self.pool.get_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM rules WHERE id=%s", (_id,))
            con.commit()

            if cur.rowcount == 0:
                raise DoesNotExists(
                    'Rule with id={id} does not exists.'.format(id=_id)
                )
        except:
            if con is not None:
                con.rollback()
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def clear(self):
        con = None
        cur = None
        try:
            con = self.pool.get_connection()
            cur = con.cursor()
            cur.execute('TRUNCATE TABLE `rules`')
            con.commit()
        except:
            if con is not None:
                con.rollback()
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()


storage_class = MySQLStorage
