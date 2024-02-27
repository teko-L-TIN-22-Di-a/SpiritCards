
from dataclasses import dataclass
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.card_engine.requirement import Requirement

@dataclass
class Action:

    PLAYER_SOURCE = "player"
    OPPONENT_SOURCE = "opponent"
    SYSTEM_SOURCE = "system"

    NEXT_PHASE = "next_phase"
    NO_ACT = "no_action"
    ON_REFRESH = "on_refresh"
    ON_END = "on_end"

    key: str
    source: str
    parameters: dict[str, any] = None