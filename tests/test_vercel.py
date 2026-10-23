"""Regression checks for the hosted request handler and shared database interface."""
import http.client
import importlib.util
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server
from cloud_database import Connection


class VercelHosting(unittest.TestCase):
    def test_cloud_rows_transactions_and_constraints(self):
        try:
            import libsql
        except ImportError:
            self.skipTest('Install requirements.txt to check the cloud driver.')
        with tempfile.TemporaryDirectory() as tmp:
            db = Connection(str(Path(tmp) / 'cloud.db'), '')
            try:
                db.execute('CREATE TABLE records(id INTEGER PRIMARY KEY, name TEXT UNIQUE)')
                db.execute('BEGIN IMMEDIATE')
                db.execute('INSERT INTO records VALUES (?, ?)', (1, 'Aye'))
                db.commit()
                row = db.execute('SELECT id, name FROM records').fetchone()
                self.assertEqual(dict(row), {'id': 1, 'name': 'Aye'})
                self.assertEqual(row[0], 1)
                self.assertEqual(row['name'], 'Aye')
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute('INSERT INTO records VALUES (?, ?)', (2, 'Aye'))
                db.execute('BEGIN IMMEDIATE')
                db.execute('INSERT INTO records VALUES (?, ?)', (2, 'Mya'))
                db.rollback()
                self.assertEqual(db.execute('SELECT COUNT(*) FROM records').fetchone()[0], 1)
            finally:
                db.close()

    def test_vercel_refuses_ephemeral_database_fallback(self):
        with patch.object(server, 'TURSO_DATABASE_URL', ''), patch.dict('os.environ', {'VERCEL': '1'}):
            with self.assertRaises(server.DomainError) as error:
                with server.connection():
                    self.fail('Vercel opened local SQLite storage.')
        self.assertEqual(error.exception.status, 503)

    def test_api_fails_closed_without_database_configuration(self):
        spec = importlib.util.spec_from_file_location('vercel_api_test', ROOT / 'api/index.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        http_server = server.ThreadingHTTPServer(('127.0.0.1', 0), module.handler)
        thread = threading.Thread(target=http_server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.object(server, 'TURSO_DATABASE_URL', ''):
                conn = http.client.HTTPConnection('127.0.0.1', http_server.server_port, timeout=5)
                try:
                    conn.request('GET', '/api/health')
                    response = conn.getresponse()
                    self.assertEqual(response.status, 503)
                    self.assertIn('not ready', json.loads(response.read())['error'])
                finally:
                    conn.close()
        finally:
            http_server.shutdown()
            http_server.server_close()

if __name__ == '__main__':
    unittest.main()
