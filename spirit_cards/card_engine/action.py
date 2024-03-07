
from dataclasses import dataclass
from spirit_cards.card_engine.requirement import Requirement

@dataclass
class Action:

    CANCEL_ACTION = "cancel_action"
    NEXT_PHASE = "next_phase"
    NO_ACT = "no_action"
    SUMMON = "summon"
    ATTACK = "attack"
    BLOCK = "block"
    CRACK = "crack"

    ON_REFRESH = "on_refresh"
    ON_END = "on_end"

    key: str
    phase_availability: list[str] = None
    placement_requirements: list[str] = None
    only_playing: bool = True
    only_as_reaction: bool = False

    requirements: list[Requirement] = None
    parameters: dict[str, any] = None
    resolve_instantly: bool = False
    
Actions = {
    Action.NEXT_PHASE: Action(Action.NEXT_PHASE),
    Action.ON_REFRESH: Action(Action.ON_REFRESH),
    Action.ON_END: Action(Action.ON_END)
}
