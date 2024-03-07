
from dataclasses import dataclass

@dataclass
class Requirement:

    TARGET_ATTACKING = "target_attacking"
    BATTLE_TARGET = "battle_target"
    TARGET_CARD = "target_card"
    TARGET_FREE_SLOT = "target_free_slot"

    MANA_COST = "mana_cost"

    key: str
    parameters: any = None
    
class Requirements:

    def mana_cost(cost: int):
        return Requirement(Requirement.MANA_COST)