
from dataclasses import dataclass

@dataclass
class Requirement:

    BATTLE_TARGET = "battle_target"
    TARGET_CARD = "target_card"
    TARGET_SLOT = "target_slot"

    MANA_COST = "mana_cost"

    COST = "cost"

    key: str
    parameters: any = None
    
class Requirements:

    def mana_cost(cost: int):
        return Requirement(Requirement.MANA_COST, { Requirement.COST: cost })