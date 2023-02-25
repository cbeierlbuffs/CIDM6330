from dataclasses import dataclass

@dataclass
class BookMark:
    id: int
    title: str
    url: str
    notes: str
    date_added: str


#newbookmark = BookMark(1,"TestTitle","hxxp://www.google.com","Test note check","02/24/2023")
#print (newbookmark)