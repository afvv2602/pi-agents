from contextlib import asynccontextmanager, closing
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI

DB = Path("/data/controller.sqlite3")


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(DB)) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.execute(
            "INSERT OR IGNORE INTO metadata VALUES (?, ?)",
            (
                "initialized_at",
                datetime.now(timezone.utc).isoformat(),
            ),
        )

    yield


app = FastAPI(
    title="Pi-Agents Controller",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    with closing(sqlite3.connect(DB)) as conn:
        initialized = conn.execute(
            "SELECT value FROM metadata WHERE key = ?",
            ("initialized_at",),
        ).fetchone()[0]

    return {
        "status": "ok",
        "service": "pi-agents-controller",
        "version": "0.1.0",
        "db_initialized_at": initialized,
    }
