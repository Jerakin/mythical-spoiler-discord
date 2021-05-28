import unittest
from app.models.set import Set
from app.models.card import Card


class TestSet(unittest.TestCase):

    set = None

    def setUp(self):
        self.set = Set('m19')

    def test_assign_cards(self):
        self.set.cards = ['card1', 'card2']

        self.assertEqual(self.set.cards, ['card1', 'card2'])

    def test_append_cards(self):
        self.set.cards = ['card1', 'card2']
        self.set.append('card3')

        self.assertEqual(self.set.cards, ['card1', 'card2', 'card3'])

    def test_name(self):
        self.assertEqual(self.set.name, 'm19')

    def test_card_length(self):
        self.set.cards = ['card1', 'card2']

        self.assertEqual(len(self.set), 2)

    def test_find_not_existing_card(self):
        result = self.set.find('non-existing-card-name')

        self.assertIsNone(result)

    def test_find_existing_card(self):
        # Arrange
        self.set.append(Card({
            'name': 'test-card-name',
            'manacost': None,
            'type': None,
            'sub_types': None,
            'set': None,
            'rules_text': None,
            'flavor': None,
            'artist': None,
            'power': None,
            'toughness': None,
            'url': None,
        }))

        # Act
        result = self.set.find('test-card-name')

        # Assert
        self.assertEqual(result.name, 'test-card-name')
        self.assertIsInstance(result, Card)
