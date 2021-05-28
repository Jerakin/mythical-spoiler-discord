import unittest
from app.models.spoiler import Spoiler
from app.models.set import Set


class TestSet(unittest.TestCase):

    spoiler = None

    def setUp(self):
        self.spoiler = Spoiler()

    def test_set_get_sets(self):
        # Arrange
        self.spoiler.set_sets(['set1', 'set2'])

        # Act
        result = self.spoiler.get_sets()

        # Assert
        self.assertEquals(result, ['set1', 'set2'])

    def test_append_get_sets(self):
        # Arrange
        self.spoiler.set_sets(['set1', 'set2'])
        self.spoiler.append_set('set3')

        # Act
        result = self.spoiler.get_sets()

        # Assert
        self.assertEquals(result, ['set1', 'set2', 'set3'])

    def test_get_sets_length(self):
        # Arrange
        self.spoiler.set_sets(['set1', 'set2'])

        # Act
        result = self.spoiler.get_sets_length()

        # Assert
        self.assertEquals(result, 2)

    def test_get_first_set(self):
        # Arrange
        self.spoiler.set_sets(['set1', 'set2'])

        # Act
        result = self.spoiler.get_first_set()

        # Assert
        self.assertEquals(result, 'set1')

    def test_find_not_existing_set(self):
        # Act
        result = self.spoiler.find_set('not-existing-set-name')

        # Assert
        self.assertFalse(result)

    def test_find_existing_set(self):
        # Arrange
        self.spoiler.append_set(Set('set-name'))

        # Act
        result = self.spoiler.find_set('set-name')

        # Assert
        self.assertEquals(result.get_name(), 'set-name')

