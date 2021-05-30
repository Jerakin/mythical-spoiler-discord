import unittest
from app.models.spoiler import Spoiler
from app.controllers.cache import Cache
from app.models.set import Set


class TCache(Cache):
    pass


class TestSet(unittest.TestCase):
    spoiler = None

    def setUp(self):
        cache = Cache()
        self.spoiler = Spoiler(cache)

    def test_find_not_existing_set(self):
        result = self.spoiler.find('not-existing-set-name')

        self.assertIsNone(result)

    def test_find_existing_set(self):
        result = self.spoiler.find('grn')

        self.assertIsNone(result)
