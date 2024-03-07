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

    # Spirit States
    just_summoned: bool = False
    alive: bool = True
    attacking: bool = False
    blocked: bool = False
    exhausted: bool = False

    def reset(self):
        self.just_summoned = False
        self.alive = True
        self.attacking = False
        self.blocked = False
        self.exhausted = False