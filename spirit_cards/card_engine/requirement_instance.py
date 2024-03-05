
from dataclasses import dataclass

from spirit_cards.card_engine.requirement import Requirement

@dataclass
class RequirementInstance:

    requirement: Requirement
    value: any

    def __init__(self, requirement: Requirement, value: any):
        self.requirement = requirement
        self.value = value