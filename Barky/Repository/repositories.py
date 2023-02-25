from repository.baserepo import AbstractRepository
from models.bookmark import BookMark

class FakeRepository(AbstractRepository):
    def __init__(self):
        self.seen = []

    def BookmarkAdd(self, bookmark: BookMark): 
        self.bookmark = bookmark
        self.seen.append(bookmark)

    def BookmarkDelete(self, id: int): 
        self.deleteindex = id
        for bm in self.seen:
            if bm.id == id:
                self.seen.remove(bm)
    
    def BookMarkList_by_Date(self):
        self.seen.sort()
    
    def BookMarkList_by_Title(self):
        self.seen.sort(key=lambda x: x.title)

#Run a little test    
newBm1 = BookMark(3,"ATest1FakeRepo","hxxp://www.fakerepo.com/test1","kitty fiddle","02/27/23")
newBm2 = BookMark(4,"FTest10FakeRepo","hxxp://www.fakerepo.com/test2","kitty fiddle","02/25/23")
newBm3 = BookMark(10,"CTest2FakeRepo","hxxp://www.fakerepo.com/test3","kitty fiddle","02/25/20")
Fr = FakeRepository()
Fr.BookmarkAdd(newBm1)
Fr.BookmarkAdd(newBm2)
Fr.BookmarkAdd(newBm3)
print("ORIGINAL\n",Fr.seen,"\n")
Fr.BookMarkList_by_Date()
print("SORT BY DATE\n",Fr.seen,"\n")
Fr.BookMarkList_by_Title()
print("SORT BY TITLE\n",Fr.seen,"\n")
Fr.BookmarkDelete(4)
print("POST DELETE:\n",Fr.seen)


'''
Run module individually like this: <topprojectdir>\python -m repository.repositories
'''