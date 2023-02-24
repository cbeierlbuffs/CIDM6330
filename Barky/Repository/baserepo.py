from abc import ABC, abstractmethod

class AbstractRepository(ABC):

    @abstractmethod
    def BookmarkAdd(self, Models.BookMark): 
        raise NotImplemented

    @abstractmethod
    def BookmarkDelete(self, Models.BookMark): 
        raise NotImplemented

    @abstractmethod
    def BookMarkList_by_Date(self, reference):
        raise NotImplemented

    @abstractmethod
    def BookMarkList_by_Title(self, reference):
        raise NotImplemented
    
