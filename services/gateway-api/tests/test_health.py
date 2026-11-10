from contextlib import closing
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import httpx

from app import main


class ControllerTests(IsolatedAsyncioTestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.db = Path(directory) / "data" / "controller.sqlite3"
        self.enterContext(patch.object(main, "DB", self.db))

    async def read_health_after_start(self):
        async with main.app.router.lifespan_context(main.app):
            transport = httpx.ASGITransport(app=main.app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/health")
                self.assertEqual(response.status_code, 200)
                return response.json()

    async def test_health_contract(self):
        result = await self.read_health_after_start()
        timestamp = datetime.fromisoformat(result.pop("db_initialized_at"))
        self.assertEqual(timestamp.utcoffset(), timedelta(0))
        self.assertEqual(result, {
            "status": "ok", "service": "pi-agents-controller", "version": "0.1.0",
        })

    async def test_initialized_at_survives_restart(self):
        first = await self.read_health_after_start()
        with closing(sqlite3.connect(self.db)) as conn:
            stored, = conn.execute(
                "SELECT value FROM metadata WHERE key = 'initialized_at'"
            ).fetchone()
        self.assertEqual(stored, first["db_initialized_at"])
        self.assertEqual(await self.read_health_after_start(), first)
