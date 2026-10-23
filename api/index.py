"""Vercel's request handler; the shared database lives on Turso, never in /tmp."""
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server as app

_ready = False
_initialization = threading.Lock()


class handler(app.Handler):
    def __init__(self, request, client_address, server):
        if not hasattr(server, 'lookups'):
            server.lookups = {}
        if not hasattr(server, 'logins'):
            server.logins = {}
        super().__init__(request, client_address, server)

    def prepare(self):
        global _ready
        try:
            if not _ready:
                with _initialization:
                    if not _ready:
                        if not app.TURSO_DATABASE_URL or not app.TURSO_AUTH_TOKEN:
                            raise RuntimeError('Hosted database configuration is required.')
                        if app.STAFF_PASSWORD == 'handshake-demo-2026':
                            raise RuntimeError('Set a private HANDSHAKE_STAFF_PASSWORD.')
                        app.initialize()
                        _ready = True
            # Serverless execution advances pending simulator jobs on requests.
            app.process_jobs()
            return True
        except Exception as error:
            print('Vercel initialization failed:', type(error).__name__, flush=True)
            self.respond({'error': 'The app database is not ready. Check deployment configuration.'}, 503)
            return False

    def do_GET(self):
        if self.prepare():
            super().do_GET()

    def do_POST(self):
        if self.prepare():
            super().do_POST()
