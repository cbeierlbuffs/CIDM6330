from repository.baserepo import AbstractRepository
from models.bookmark import BookMark

class FakeRepository(AbstractRepository):
    def __init__(self):
        self.seen = []
    
    def BookmarkGetNextid(self):
        maxid = 0
        for bm in self.seen:
            if bm.id > maxid:
                maxid = bm.id
        nextid = maxid + 1
        return nextid

    def BookmarkAdd(self, bookmark: BookMark): 
        bookmark.id = self.BookmarkGetNextid()
        self.bookmark = bookmark
        self.seen.append(bookmark)

    def BookmarkDelete(self, id: int): 
        for bm in self.seen:
            if bm.id == id:
                self.seen.remove(bm)
    
    def BookmarkList_by_Date(self):
        self.seen.sort()
    
    def BookmarkList_by_Title(self):
        self.seen.sort(key=lambda x: x.title)

    def BookmarkRetrieve(self, id: int):
        for bm in self.seen:
            if bm.id == id:
                return bm       
    
    def BookmarkClear(self):
        self.seen.clear()
    
    
#run module individually like this: <topprojectdir>\python -m repository.repositories