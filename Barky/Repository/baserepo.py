from abc import ABC, abstractmethod
from Models.models import BookMark

class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()

    @abstractmethod
    def BookmarkAdd(self, bookmark: models): 
        raise NotImplemented

    @abstractmethod
    def BookmarkDelete(self, bookmark: models): 
        raise NotImplemented

    @abstractmethod
    def BookMarkList_by_Date(self, reference):
        raise NotImplemented

    @abstractmethod
    def BookMarkList_by_Title(self, reference):
        raise NotImplemented
    
