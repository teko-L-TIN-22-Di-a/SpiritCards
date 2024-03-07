from dataclasses import dataclass
from spirit_cards.card_engine.card import Card

@dataclass
class Slot:

    HAND_SLOT = "hand"
    SUPPORT_SLOT = "support"
    BATTLE_SLOT = "battle"
    GRAVE_SLOT = "grave"

    type: str = None
    card: Card = None

    active: bool = True