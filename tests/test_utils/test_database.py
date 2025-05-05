import pytest
from app.database import Database

def test_initialize_sets_engine(monkeypatch):
    # Reset engine
    Database._engine = None

    from sqlalchemy.ext.asyncio import AsyncEngine

    # Actually create a valid async engine to simulate the real behavior
    Database.initialize("sqlite+aiosqlite:///test.db", echo=False)

    assert isinstance(Database._engine, AsyncEngine)
