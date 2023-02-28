import pytest
from database import DatabaseManager

@pytest.fixture
def dbm():
    dbm = DatabaseManager(":memory:")
    return dbm

@pytest.fixture
def table_name():
    table_name = "BOOKMARKS"
    return table_name

@pytest.fixture
def table_structure():
    table_structure = {
        "id":"INTEGER PRIMARY KEY AUTOINCREMENT",
        "title":"TEXT NOT NULL",
        "url": "TEXT NOT NULL",
        "notes":"TEXT",
        "date_added":"TEXT NOT NULL"
    }
    return table_structure