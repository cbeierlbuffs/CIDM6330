import pytest
from database import DatabaseManager

@pytest.fixture
def dbm():
    dbm = DatabaseManager(":memory:")
    return dbm

@pytest.fixture
def table_name():
    table_name = "bookmarks"
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

@pytest.fixture
def record1():
    record1 = {
        "title" : "Atesttitle",
        "url" :"hxxp://www.test.url/",
        "notes":"testnotes",
        "date_added":"02/12/22"
    }
    return record1

@pytest.fixture
def record2():
    record2 = {
        "title" : "Ctesttitle",
        "url" :"hxxp://www.test.url/",
        "notes":"testnotes",
        "date_added":"02/10/22"
    }
    return record2

@pytest.fixture  
def record3():
    record3 = {
        "title" : "Btesttitle",
        "url" :"hxxp://www.test.url/",
        "notes":"testnotes",
        "date_added":"02/10/23"
    }
    return record3  