from baserepo import AbstractRepository

class FakeRepository(AbstractRepository):
    def __init__(self):
        self.seen = set()


Fr = FakeRepository()