from dataclasses import dataclass
@dataclass
class BookMark:
    id: int
    title: str
    url: str
    notes: str
    date_added: str

