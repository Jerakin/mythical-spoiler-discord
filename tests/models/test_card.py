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

    def test_name(self):
        self.assertEqual(self.card.name, 'Keldon Warcaller')

    def test_normalized_name_from_name(self):
        self.assertEqual(self.card.normalized_name, 'keldonwarcaller')

    def test_normalized_name_from_url(self):
        self.card.name = None

        self.assertEqual(self.card.normalized_name, 'keldonwarcaller')

    def test_mana_cost(self):
        self.assertEqual(self.card.mana_cost, '5GBR')

    def test_mana_value(self):
        self.assertEqual(self.card.mana_value, 8)

    def test_hybrid_mana(self):
        self.card.mana_cost = "[G/U][G/U][G/U][G/U]"
        self.assertEqual(self.card.mana_value, 4)

    def test_mixed_hybrid_mana(self):
        self.card.mana_cost = "2G[G/U]2U"
        self.assertEqual(self.card.mana_value, 7)

    def test_type(self):
        self.assertEqual(self.card.type, 'Legendary Creature')

    def test_subtypes(self):
        self.assertEqual(self.card.sub_types, ['Elemental'])

    def test_set(self):
        self.assertEqual(self.card.set, 'dom')

    def test_rules_text(self):
        self.assertEqual(self.card.rules_text, 'Creatures you control have haste. Cascade, cascade (When you cast this spell, exile cards from the top of your library until you exile a nonland card that costs less. You may cast it without paying its mana cost. Put the exiled cards on the bottom of your library in a random order. Then do it again.)')

    def test_flavor(self):
        self.assertEqual(self.card.flavor, 'Test flavor')

    def test_artist(self):
        self.assertEqual(self.card.artist, 'Thomas M. Baxa')

    def test_power(self):
        self.assertEqual(self.card.power, '7')

    def test_toughness(self):
        self.assertEqual(self.card.toughness, '5')

    def test_image_filename_from_name(self):
        self.assertEqual(self.card.get_image_filename(), 'dom_keldonwarcaller')

    def test_image_filename_from_url(self):
        self.card.name = None

        self.assertEqual(self.card.get_image_filename(), 'dom_keldonwarcaller90')