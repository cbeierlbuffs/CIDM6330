from dataclasses import dataclass
from datetime import datetime

@dataclass
class BookMark:
    id: int
    title: str
    url: str
    notes: str
    date_added: str

    def __lt__(self, other):
        return datetime.strptime(self.date_added, '%m/%d/%y') < datetime.strptime(other.date_added, '%m/%d/%y')


#newbookmark = BookMark(1,"TestTitle","hxxp://www.google.com","Test note check","02/24/2023")
#print (newbookmark)