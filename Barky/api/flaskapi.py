# python imports
# third-party imports
from flask import Flask
from markupsafe import escape
# your own imports
from repository.repositories import FakeRepository
from models.bookmark import BookMark

from tests.test_repositories import load_bookmarks

Repo = FakeRepository()

app = Flask(__name__)



@app.route("/")
def initialize_and_root():
    load_bookmarks(Repo)
    return "Charles Barky App"

@app.route("/listall")
def list_all_bookmarks():
    Repo.BookmarkList_by_id()
    return Repo.seen

@app.route("/listallbydate")
def list_all_bookmarks_by_date():
    Repo.BookmarkList_by_Date()
    return Repo.seen

@app.route("/listallbytitle")
def list_all_bookmarks_by_title():
    Repo.BookmarkList_by_Title()
    return Repo.seen

@app.route("/clearall")
def clear_all_bookmarks():
    beginning_records = len(Repo.seen)
    Repo.BookmarkClear()
    remaining_records = len(Repo.seen)
    return_string = "Record Count: Started:" + str(beginning_records) + " Now: " + str(remaining_records)
    return return_string
# run flask using  flask --app api.flaskapi run --debug