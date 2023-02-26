from dataclasses import dataclass
from datetime import datetime

@dataclass
class BookMark:
    id: int
    title: str
    url: str
    notes: str
    date_added: str = datetime.now().strftime('%m/%d/%y')

    def __lt__(self, other):
        return datetime.strptime(self.date_added, '%m/%d/%y') < datetime.strptime(other.date_added, '%m/%d/%y')
