import re
from app.models.base import Base
from app.utils import slugify


class Card(Base):
    def __init__(self, c, new=False):
        super(Card, self).__init__()
        self.name = c['name']
        self.mana_cost = c['manacost']
        self.type = c['type']
        self.sub_types = c['sub_types']
        self.set = c['set']
        self.rules_text = c['rules_text']
        self.flavor = c['flavor']
        self.artist = c['artist']
        self.power = c['power']
        self.toughness = c['toughness']
        self.url = c['url']

        self.new = new

    @property
    def normalized_name(self):
        if self.name:
            return slugify(self.name).lower()
        else:
            return slugify(self.url.replace(self.config['domain'] + '/' + self.set + '/cards/', '').replace('.html', ''))

    @property
    def mana_value(self):
        result = re.findall(r'([WUBRGC])|(\[[WUBRGC\/]+\])|([0-9]+)', self.mana_cost)
        result = [part for groups in result for part in groups if part]
        amount = 0
        for x in result:
            if x.isnumeric():
                amount += int(x)
            else:
                amount += 1
        return amount

    def get_image_filename(self):
        if self.name:
            return self.set + '_' + self.normalized_name
        else:
            return self.set + '_' + self.normalized_name + '90'
