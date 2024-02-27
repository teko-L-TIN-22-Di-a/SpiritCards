
from dataclasses import dataclass
from spirit_cards.card_engine.card_player import CardPlayer

@dataclass
class Action:

    NO_ACT = "no_action"

    key: str
    source: CardPlayer
    parameters: any