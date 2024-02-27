
from dataclasses import dataclass

from spirit_cards.card_engine.action import Action

@dataclass
class Card:

    actions: list[Action]

    asset_key: str
    attack: int
    health: int
