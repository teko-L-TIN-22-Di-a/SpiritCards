from dataclasses import dataclass
from spirit_cards.card_engine.card import Card

@dataclass
class Slot:
    card: Card = None