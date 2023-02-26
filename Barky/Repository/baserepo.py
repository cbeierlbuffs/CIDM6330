from abc import ABC, abstractmethod
from models.bookmark import BookMark

class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()

    @abstractmethod
    def BookmarkAdd(self, bookmark: BookMark): 
        raise NotImplemented

    @abstractmethod
    def BookmarkDelete(self, int): 
        raise NotImplemented

    @abstractmethod
    def BookmarkList_by_Date(self):
        raise NotImplemented

    @abstractmethod
    def BookmarkList_by_Title(self):
        raise NotImplemented
    
    @abstractmethod
    def BookmarkRetrieve(self, int):
        raise NotImplemented
