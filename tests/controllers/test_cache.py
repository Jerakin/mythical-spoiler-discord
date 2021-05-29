import unittest
from app.controllers.cache import Cache
from app.models.spoiler import Spoiler


class TestCache(unittest.TestCase):

    cache = None

    def setUp(self):
        self.cache = Cache(Spoiler())
        self.cache.update_cache()

    def test_has_set(self):
        # Act
        result = self.cache.has_set('grn')

        # Assert
        self.assertTrue(result)

    def test_has_not_set(self):
        # Act
        result = self.cache.has_set('notexistingset')

        # Assert
        self.assertFalse(result)

    def test_has_card(self):
        # Act
        result = self.cache.has_card('grn', 'aureliaexemplarofjustice')

        # Assert
        self.assertTrue(result)

    def test_has_not_card_by_card(self):
        # Act
        result = self.cache.has_card('grn', 'notexistingcard')

        # Assert
        self.assertFalse(result)

    def test_has_not_card_by_set(self):
        # Act
        result = self.cache.has_card('notexistingset', 'aureliaexemplarofjustice')

        # Assert
        self.assertFalse(result)

    def test_tsr(self):
        # Act
        result = self.cache.has_card('tsr', 'boom // burst')

        # Assert
        self.assertFalse(result)
