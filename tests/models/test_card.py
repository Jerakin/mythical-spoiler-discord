import unittest
from app.models.card import Card


class TestCard(unittest.TestCase):

    card = None

    def setUp(self):
        self.card = Card({
            'name': 'Keldon Warcaller',
            'manacost': '5GBR',
            'type': 'Legendary Creature',
            'sub_types': [
                'Elemental'
            ],
            'set': 'dom',
            'rules_text': 'Creatures you control have haste. Cascade, cascade (When you cast this spell, exile cards from the top of your library until you exile a nonland card that costs less. You may cast it without paying its mana cost. Put the exiled cards on the bottom of your library in a random order. Then do it again.)',
            'flavor': 'Test flavor',
            'artist': 'Thomas M. Baxa',
            'power': '7',
            'toughness': '5',
            'url': 'http://mythicspoiler.com/dom/cards/keldonwarcaller.html',
        })

    def test_get_name(self):
        # Act
        result = self.card.get_name()

        # Assert
        self.assertEquals(result, 'Keldon Warcaller')

    def test_get_normalized_name_from_name(self):
        # Act
        result = self.card.get_normalized_name()

        # Assert
        self.assertEquals(result, 'keldonwarcaller')

    def test_get_normalized_name_from_url(self):
        # Arrange
        self.card.name = None

        # Act
        result = self.card.get_normalized_name()

        # Assert
        self.assertEquals(result, 'keldonwarcaller')

    def test_get_manacost(self):
        # Act
        result = self.card.get_manacost()

        # Assert
        self.assertEquals(result, '5GBR')

    def test_get_cmc(self):
        # Act
        result = self.card.get_cmc()

        # Assert
        self.assertEquals(result, 8)

    def test_get_type(self):
        # Act
        result = self.card.get_type()

        # Assert
        self.assertEquals(result, 'Legendary Creature')

    def test_get_subtypes(self):
        # Act
        result = self.card.get_sub_types()

        # Assert
        self.assertEquals(result, ['Elemental'])

    def test_get_subtypes_string(self):
        # Act
        result = self.card.get_sub_types_string()

        # Assert
        self.assertEquals(result, 'Elemental ')

    def test_get_set(self):
        # Act
        result = self.card.get_set()

        # Assert
        self.assertEquals(result, 'dom')

    def test_get_rules_text(self):
        # Act
        result = self.card.get_rules_text()

        # Assert
        self.assertEquals(result, 'Creatures you control have haste. Cascade, cascade (When you cast this spell, exile cards from the top of your library until you exile a nonland card that costs less. You may cast it without paying its mana cost. Put the exiled cards on the bottom of your library in a random order. Then do it again.)')

    def test_get_flavor(self):
        # Act
        result = self.card.get_flavor()

        # Assert
        self.assertEquals(result, 'Test flavor')

    def test_get_artist(self):
        # Act
        result = self.card.get_artist()

        # Assert
        self.assertEquals(result, 'Thomas M. Baxa')

    def test_get_power(self):
        # Act
        result = self.card.get_power()

        # Assert
        self.assertEquals(result, '7')

    def test_get_toughness(self):
        # Act
        result = self.card.get_toughness()

        # Assert
        self.assertEquals(result, '5')

    def test_get_image_filename_from_name(self):
        # Act
        result = self.card.get_image_filename()

        # Assert
        self.assertEquals(result, 'dom_keldonwarcaller')

    def test_get_image_filename_from_url(self):
        # Arrange
        self.card.name = None

        # Act
        result = self.card.get_image_filename()

        # Assert
        self.assertEquals(result, 'dom_keldonwarcaller90')