import unittest
from app.models.set import Set
from app.models.card import Card


class TestSet(unittest.TestCase):

    set = None

    def setUp(self):
        self.set = Set('m19')

    def test_set_get_cards(self):
        # Arrange
        self.set.set_cards(['card1', 'card2'])

        # Act
        result = self.set.get_cards()

        # Assert
        self.assertEquals(result, ['card1', 'card2'])

    def test_append_get_cards(self):
        # Arrange
        self.set.set_cards(['card1', 'card2'])
        self.set.append_card('card3')

        # Act
        result = self.set.get_cards()

        # Assert
        self.assertEquals(result, ['card1', 'card2', 'card3'])

    def test_get_name(self):
        # Act
        result = self.set.get_name()

        # Assert
        self.assertEquals(result, 'm19')

    def test_get_card_length(self):
        # Arrange
        self.set.set_cards(['card1', 'card2'])

        # Act
        result = self.set.get_cards_length()

        # Assert
        self.assertEquals(result, 2)

    def test_get_first_card(self):
        # Arrange
        self.set.set_cards(['card1', 'card2'])

        # Act
        result = self.set.get_first_card()

        # Assert
        self.assertEquals(result, 'card1')

    def test_find_not_existing_card(self):
        # Act
        result = self.set.find_card('non-existing-card-name')

        # Assert
        self.assertFalse(result)

    def test_find_existing_card(self):
        # Arrange
        self.set.append_card(Card({
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
        result = self.set.find_card('test-card-name')

        # Assert
        self.assertEquals(result.get_name(), 'test-card-name')
        self.assertIsInstance(result, Card)




