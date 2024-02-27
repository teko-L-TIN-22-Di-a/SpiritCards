
from dataclasses import dataclass
from spirit_cards.card_engine.card_player import CardPlayer


@dataclass
class Requirement:

    TARGET_CARD = "target_card"
    TARGET_SLOT = "target_slot"

    key: str
    source: CardPlayer
    parameters: any