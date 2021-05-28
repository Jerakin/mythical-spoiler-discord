import json
from pathlib import Path
config = Path(__file__).parent.parent.parent / "config.json"


class Base:
    config = []

    def __init__(self):
        with config.open() as file:
            self.config = json.load(file)
