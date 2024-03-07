
from typing import Callable
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.action_instance import ActionInstance
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.requirement_instance import RequirementInstance
from spirit_cards.card_engine.slot import Slot


class RequirementHandler:

    context: BoardContext
    resolve_map: dict[str, Callable[[RequirementInstance, ActionInstance], None]]

    def __init__(self, context: BoardContext):
        self.context = context
        self.resolve_map = {
            Requirement.MANA_COST: self.handle_mana_cost,
            Requirement.TARGET_FREE_SLOT: self.handle_target_free_slot,
            Requirement.TARGET_ATTACKING: self.handle_target_attacking
        }

    def handle_mana_cost(self, requirement: RequirementInstance, instance: ActionInstance):
        cost = instance.slot.card.cost
        if(instance.source.resources < cost):
            return
        requirement.value = cost

    def handle_target_attacking(self, requirement: RequirementInstance, instance: ActionInstance):
        player = self.context.player

        slots_to_check = [
            *player.battle_slots,
            *player.support_slots
        ]

        for slot in slots_to_check:
            if(not slot.attacking or slot.blocked): 
                continue

            slot.active = True

    def handle_target_free_slot(self, requirement: RequirementInstance, instance: ActionInstance):
        player = instance.source

        slots_to_check = [
            *player.battle_slots,
            *player.support_slots
        ]

        for slot in slots_to_check:
            if(slot.card is not None): 
                continue

            slot.active = True

    def handle_requirement(self, requirement: RequirementInstance, instance: ActionInstance) -> None:

        if(requirement.requirement.key not in self.resolve_map):
            print(f"RequirementHandler | No Resolver for {requirement.requirement.key} ignoring for now.")
            return

        self.resolve_map[requirement.requirement.key](requirement, instance)