import pytest

from app.config.database import get_db


@pytest.fixture
def db():
    yield from get_db()