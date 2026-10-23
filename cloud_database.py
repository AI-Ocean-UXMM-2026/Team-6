"""Use the cloud libSQL primary while preserving the app's SQLite row interface."""
import sqlite3


class Row:
    def __init__(self, columns, values):
        self._columns = columns
        self._values = values

    def keys(self):
        return self._columns

    def __getitem__(self, key):
        return self._values[self._columns.index(key)] if isinstance(key, str) else self._values[key]

    def __iter__(self):
        return iter(self._values)


class Cursor:
    def __init__(self, cursor):
        self._cursor = cursor
        self._columns = tuple(column[0] for column in (cursor.description or ()))

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def fetchone(self):
        value = self._cursor.fetchone()
        return None if value is None else Row(self._columns, value)

    def fetchall(self):
        return [Row(self._columns, value) for value in self._cursor.fetchall()]

    def __iter__(self):
        while True:
            row = self.fetchone()
            if row is None:
                break
            yield row


class Connection:
    def __init__(self, url, token):
        import libsql
        self._connection = libsql.connect(url, auth_token=token, isolation_level=None)

    def execute(self, sql, parameters=()):
        try:
            return Cursor(self._connection.execute(sql, parameters))
        except ValueError as error:
            # libsql reports SQLite failures as ValueError, including trigger RAISEs.
            message = str(error)
            integrity_failure = any(text in message.lower() for text in (
                'constraint failed', 'append-only', 'immutable', 'financial jobs cannot be deleted',
            ))
            error_class = sqlite3.IntegrityError if integrity_failure else sqlite3.DatabaseError
            raise error_class(message) from error

    def executemany(self, sql, parameters):
        return Cursor(self._connection.executemany(sql, list(parameters)))

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()
