
from dataclasses import dataclass
from spirit_cards.card_engine.requirement import Requirement, RequirementInstance

@dataclass
class ActionInstance:

    PLAYER_SOURCE = "player"
    OPPONENT_SOURCE = "opponent"
    SYSTEM_SOURCE = "system"

    key: str
    source: str
    parameters: dict[str, any] = None
    requirements: list[RequirementInstance] = None

@dataclass
class Action:

    NEXT_PHASE = "next_phase"
    NO_ACT = "no_action"
    SUMMON = "summon"
    ATTACK = "attack"
    CRACK = "crack"

    ON_REFRESH = "on_refresh"
    ON_END = "on_end"

    key: str
    availability: list[str] = None
    requirements: list[Requirement] = None
    parameters: dict[str, any] = None

    def new_instance(self, source: str) -> ActionInstance:

        return ActionInstance(self.key, source, self.parameters, [x.new_instance(None) for x in self.requirements or []])
    
Actions = {
    Action.ON_REFRESH: Action(Action.ON_REFRESH),
    Action.ON_END: Action(Action.ON_END)
}
