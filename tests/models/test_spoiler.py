import unittest
from app.models.spoiler import Spoiler
from app.models.set import Set


class TestSet(unittest.TestCase):

    spoiler = None

    def setUp(self):
        self.spoiler = Spoiler()

    def test_assign_sets(self):
        self.spoiler.sets = ['set1', 'set2']

        self.assertEqual(self.spoiler.sets, ['set1', 'set2'])

    def test_append_sets(self):
        self.spoiler.sets = ['set1', 'set2']

        self.spoiler.append('set3')

        self.assertEqual(self.spoiler.sets, ['set1', 'set2', 'set3'])

    def test_sets_length(self):
        self.spoiler.sets = ['set1', 'set2']

        self.assertEqual(len(self.spoiler.sets), 2)

    def test_find_not_existing_set(self):
        result = self.spoiler.find('not-existing-set-name')

        self.assertIsNone(result)

    def test_find_existing_set(self):
        self.spoiler.append(Set('set-name'))

        result = self.spoiler.find('set-name')

        self.assertEqual(result.name, 'set-name')

