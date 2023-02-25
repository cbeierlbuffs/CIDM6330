from repository.baserepo import AbstractRepository

class FakeRepository(AbstractRepository):
    def __init__(self):
        self.seen = set()


Fr = FakeRepository()

'''
Run module individually like this: python -m repository.repositories
'''