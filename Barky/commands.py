"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC, abstractmethod
from datetime import datetime

import requests

from database import DatabaseManager

# module scope
db = DatabaseManager("bookmarks.db")


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError("A command must implement the execute method")


class CreateBookmarksTableCommand(Command):
    """
    uses the DatabaseManager to create the bookmarks table
    """

    def execute(self, data=None):
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand(Command):
    """
    This class will:

    1. Expect a dictionary containing the title, URL, and (optional) notes information for a bookmark.
    2. Add the current datetime to the dictionary as date_added.
    3. Insert the data into the bookmarks table using the DatabaseManager.add method.
    4. Return a success message that will eventually be displayed by the presentation layer.
    """

    def execute(self, data, timestamp=None):
        data["date_added"] = datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand(Command):
    """
    We need to review the bookmarks in the database.
    To do so, this class will:
    1. Accept the column to order by, and save it as an instance attribute.
    2. Pass this information along to db.select in its execute method.
    3. Return the result (using the cursor’s .fetchall() method) because select is a query.
    """

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return db.select("bookmarks", order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    """
    We also need to remove bookmarks.
    """

    def execute(self, data):
        db.delete("bookmarks", {"id": data})
        return "Bookmark deleted!"


class ImportGitHubStarsCommand(Command):
    """
    Import starred repos in Github - credit Dane Hillard
    """
    def _extract_bookmark_info(self, repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data["github_username"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"
        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp,
                )

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class EditBookmarkCommand(Command):
    def execute(self, data):
        db.update("bookmarks", data)
        return "Bookmark updated!"


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()

import pytest

def test_CreateBookmarksTableCommand(table_name):
    CreateBookmarksTableCommand()
    stmt_cursor = db._execute(
        f'''
        SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';
        '''
    )
    table_count = stmt_cursor.fetchone()[0]
    db.connection.close
    assert table_count == 1

def test_AddBookmarkCommand(table_name, record1):
    del record1['date_added']
    command = AddBookmarkCommand()
    resp = command.execute(record1)
    assert resp == "Bookmark added!"

def test_ListBookmarksCommand(table_name, table_structure, record1, record2, record3):
    db.drop_table(table_name)
    db.connection.commit()
    db.create_table(table_name,table_structure)
    db.add(table_name,record1)
    db.add(table_name,record2)
    db.add(table_name,record3)
    db.connection.commit()
    command = ListBookmarksCommand()
    resp = command.execute('title')
    assert resp[0][1] == 'Ctesttitle'

def test_DeleteBookmarkCommand(table_name, table_structure, record1, record2, record3):
    db.drop_table(table_name)
    db.connection.commit()
    db.create_table(table_name,table_structure)
    db.add(table_name,record1)
    db.add(table_name,record2)
    db.add(table_name,record3)
    db.connection.commit()
    command = DeleteBookmarkCommand()
    resp = command.execute(2)
    assert resp == 'Bookmark deleted!'

def test_ImportGitHubStarsCommand():
    command = ImportGitHubStarsCommand()
    data = {
        'github_username': 'cbeierlbuffs'
    }
    resp = command.execute(data)
    assert resp == 'Imported 0 bookmarks from starred repos!'

def test_EditBookmarkCommand(table_name, table_structure, record1):
    data = {
        'id' : '1',
        'notes' : 'updated notes field'
    }
    db.drop_table(table_name)
    db.connection.commit()
    db.create_table(table_name,table_structure)
    db.add(table_name,record1)
    command = EditBookmarkCommand()
    resp = command.execute(data)
    assert resp == 'Bookmark updated!'

def test_QuitCommand():
    with pytest.raises(SystemExit) as e:
        command = QuitCommand()
        command.execute()
    assert e.type == SystemExit