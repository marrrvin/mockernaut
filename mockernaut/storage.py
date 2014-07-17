
from flask.json import dumps
from flask.json import loads

from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import cursor

from mockernaut.errors import DoesNotExist


class MySQLCursorDict(cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))

        return None


def _row_from_rule(rule):
    return (
        rule['request']['path'],
        dumps(rule['request']),
        dumps(rule['response'])
    )


def _rule_from_row(data):
    return {
        'id': data['id'],
        'request': loads(data['request']),
        'response': loads(data['response'])
    }


class MySQLStorage(object):
    DoesNotExist = DoesNotExist

    def __init__(self, **kwargs):
        self.pool = MySQLConnectionPool(**kwargs)

    def get_list_by_path(self, path):
        con = None
        cur = None

        try:
            con = self.pool.get_connection()

            cur = con.cursor(cursor_class=MySQLCursorDict)
            cur.execute('SELECT * FROM rules WHERE path=%s', (path,))

            rows = cur.fetchall()
            if not rows:
                raise DoesNotExist(
                    'Rule with path={path} does not exist.'.format(path=path)
                )

            return [_rule_from_row(row) for row in rows]
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
            cur.execute('SELECT * FROM rules WHERE id=%s', (_id,))

            row = cur.fetchone()
            if not row:
                raise DoesNotExist(
                    'Rule with id={id} does not exist.'.format(id=_id)
                )

            return _rule_from_row(row)
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
            cur.execute('SELECT * FROM `rules`')

            rows = cur.fetchall()

            return [_rule_from_row(row) for row in rows]
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()

    def create(self, rule):
        sql = 'INSERT INTO `rules` (`path`, `request`, `response`)' \
              'VALUES (%s, %s, %s)'

        con = None
        cur = None

        try:
            con = self.pool.get_connection()
            cur = con.cursor(cursor_class=MySQLCursorDict)

            cur.execute(sql, _row_from_rule(rule))
            rule['id'] = cur.lastrowid

            con.commit()

            return rule
        except:
            if con is not None:
                con.rollback()

            raise
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
            cur.execute('DELETE FROM rules WHERE id=%s', (_id,))
            con.commit()

            if cur.rowcount == 0:
                raise DoesNotExist(
                    'Rule with id={id} does not exist.'.format(id=_id)
                )
        except:
            if con is not None:
                con.rollback()

            raise
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

            raise
        finally:
            if cur is not None:
                cur.close()
            if con is not None:
                con.close()


storage_class = MySQLStorage
