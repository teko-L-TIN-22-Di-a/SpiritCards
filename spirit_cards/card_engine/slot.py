from dataclasses import dataclass
from spirit_cards.card_engine.card import Card

_current_slot_id = 0

@dataclass
class Slot:

    _slot_id: int = 0

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

    def __init__(
            self,
            type: str = None,
            card: Card = None):
        global _current_slot_id
        _current_slot_id += 1
        self._slot_id = _current_slot_id
        self.type = type
        self.card = card

    def __eq__(self, other):
        return self._slot_id == other._slot_id

    def reset(self):
        self.just_summoned = False
        self.alive = True
        self.attacking = False
        self.blocked = False
        self.exhausted = False