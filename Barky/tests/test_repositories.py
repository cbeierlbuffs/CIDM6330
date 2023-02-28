from repository.baserepo import AbstractRepository
from repository.repositories import FakeRepository
from models.bookmark import BookMark

import pytest

Repo = FakeRepository()

def load_bookmarks(Repo: AbstractRepository):
    Repo.BookmarkClear()   
    newBm1 = BookMark(Repo.BookmarkGetNextid(),"BTest1FakeRepo","hxxp://www.fakerepo.com/test1","kitty fiddle")
    newBm2 = BookMark(Repo.BookmarkGetNextid(),"ATest2FakeRepo","hxxp://www.fakerepo.com/test2","kitty fiddle")
    Repo.BookmarkAdd(newBm1)
    Repo.BookmarkAdd(newBm2)

def test_BookmarkClear():
    load_bookmarks(Repo)
    Repo.BookmarkClear()
    assert len(Repo.seen) == 0

def test_BookmarkGetNextid():
    Repo.BookmarkClear()
    assert Repo.BookmarkGetNextid() == 1

def test_BookmarkAdd():
    Repo.BookmarkClear()   
    newBm1 = BookMark(Repo.BookmarkGetNextid(),"ATest1FakeRepo","hxxp://www.fakerepo.com/test1","kitty fiddle")
    Repo.BookmarkAdd(newBm1)
    assert len(Repo.seen) == 1

def test_BookmarkDelete():
    load_bookmarks(Repo)
    Repo.BookmarkDelete(1)
    assert len(Repo.seen) == 1

def test_BookmarkRetrieve():
    load_bookmarks(Repo)
    bookmark = Repo.BookmarkRetrieve(2)
    assert bookmark.title == "ATest2FakeRepo"

def test_BookmarkList_by_Title():
    load_bookmarks(Repo)
    Repo.BookmarkList_by_Title()
    bookmark = Repo.seen[1]
    assert bookmark.title == "BTest1FakeRepo"

