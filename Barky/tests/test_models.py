from models.bookmark import BookMark
from repository.repositories import FakeRepository

import pytest

Fr = FakeRepository()

def test_bookmark_struct():
   bookmarker_new = BookMark(Fr.BookmarkGetNextid(),"Title Test", "hxxp://test.com/testurl","Test Note")
   assert bookmarker_new.title == "Title Test"