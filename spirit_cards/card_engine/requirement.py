
from dataclasses import dataclass

@dataclass
class RequirementInstance:

    key: str
    parameters: any
    value: any

@dataclass
class Requirement:

    BATTLE_TARGET = "battle_target"
    TARGET_CARD = "target_card"
    TARGET_SLOT = "target_slot"

    MANA_COST = "mana_cost"

    COST = "cost"

    key: str
    parameters: any

    def new_instance(self, value: any) -> RequirementInstance:
        return RequirementInstance(self.key, value, self.parameters)
    
class Requirements:

    def mana_cost(cost: int):
        return Requirement(Requirement.MANA_COST, { Requirement.COST })