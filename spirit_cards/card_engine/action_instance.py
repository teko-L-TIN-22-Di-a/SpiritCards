from dataclasses import dataclass
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.card_player import CardPlayer
from spirit_cards.card_engine.requirement_instance import RequirementInstance
from spirit_cards.card_engine.slot import Slot


@dataclass
class ActionInstance:

    action: Action
    slot: Slot
    source: CardPlayer = None # None means system is the source
    parameters: dict[str, any] = None
    requirements: list[RequirementInstance] = None

    def __init__(self, action: Action, source: str, slot: Slot):
        self.action = action
        self.source = source
        self.slot = slot
        self.requirements = []

    def is_complete(self) -> bool:
        return len(self.requirements) == len(self.action.requirements or [])