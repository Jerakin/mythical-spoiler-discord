import unittest
from app.controllers.cache import Cache


class TestCache(unittest.TestCase):
    cache = None

    def setUp(self):
        self.cache = Cache()

    def test_has_set(self):
        result = self.cache.has_set('grn')

        self.assertTrue(result)

    def test_has_not_set(self):
        result = self.cache.has_set('notexistingset')

        self.assertFalse(result)

    def test_has_card(self):
        result = self.cache.has_card('grn', 'aureliaexemplarofjustice')

        self.assertTrue(result)

    def test_has_not_card_by_card(self):
        result = self.cache.has_card('grn', 'notexistingcard')

        self.assertFalse(result)

    def test_has_not_card_by_set(self):
        result = self.cache.has_card('notexistingset', 'aureliaexemplarofjustice')

        self.assertFalse(result)

    def test_tsr(self):
        result = self.cache.has_card('tsr', 'boom // burst')

        self.assertFalse(result)
