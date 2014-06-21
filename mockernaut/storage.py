
from json import dumps
from json import loads

from mysql.connector import connect
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
        self.cnx = connect(**kwargs)

    def get_by_id(self, _id):
        cursor = self.cnx.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules WHERE id=%s", (_id,))

        return self.make_rule(cursor.fetchone())

    def get_all(self):
        cursor = self.cnx.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules")

        return [self.make_rule(item) for item in cursor.fetchall()]

    def get_by_path(self, path):
        cursor = self.cnx.cursor(cursor_class=MySQLCursorDict)

        cursor.execute("SELECT * FROM rules WHERE path=%s", (path,))

        return self.make_rule(cursor.fetchone())

    def make_rule(self, data):
        if not data:
            raise DoesNotExists

        path = data.pop('path')
        data['request'] = loads(data['request'])

        data['response'] = loads(data['response'])

        return data

    def add(self, item):
        cursor = self.cnx.cursor()
        cursor.execute(
            "INSERT INTO `rules` (`path`, `request`, `response`) VALUES (%s, %s, %s)",
            (item['request']['path'], dumps(item['request']), dumps(item['response']))
        )
        item['id'] = cursor.lastrowid

        return item

    def delete_by_id(self, _id):
        cursor = self.cnx.cursor()
        cursor.execute("DELETE FROM rules WHERE id=%s", (_id,))

        if cursor.rowcount == 0:
            raise DoesNotExists

    def get_by_request(self, request):
        raise NotImplementedError


storage_class = MySQLStorage
