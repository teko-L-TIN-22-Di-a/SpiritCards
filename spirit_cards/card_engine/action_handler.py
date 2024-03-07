
from typing import Callable
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.action_instance import ActionInstance
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.slot import Slot


class ActionHandler:

    context: BoardContext
    resolve_map: dict[str, Callable[[ActionInstance], None]]

    def __init__(self, context: BoardContext):
        self.context = context
        self.resolve_map = {
            Action.SUMMON: self.resolve_summon,
            Action.CRACK: self.resolve_crack,
            Action.ATTACK: self.resolve_attack,
            Action.BLOCK: self.resolve_block
        }

    def resolve_attack(self, instance: ActionInstance):
        tmpCard = instance.slot.card
        opponent = self.context.opponent

        if(instance.slot.blocked):
            return    

        opponent.health -= tmpCard.attack

        instance.slot.exhausted = True
        instance.slot.attacking = False
        instance.slot.blocked = False

    def resolve_block(self, instance: ActionInstance):

        blocked_slot: Slot = next(
            requirement.value for requirement in instance.requirements 
            if requirement.requirement.key == Requirement.TARGET_ATTACKING
        )
        blocking_card = instance.slot.card
        opponent_card = blocked_slot.card

        blocked_slot.blocked = True

        if(blocking_card.health <= opponent_card.attack):
            instance.slot.alive = False

        if(opponent_card.health <= blocking_card.attack):
            blocked_slot.alive = False

    def resolve_summon(self, instance: ActionInstance):
        
        tmpCard = instance.slot.card
        player = instance.source
        target_slot: Slot = next(
            requirement.value for requirement in instance.requirements 
            if requirement.requirement.key == Requirement.TARGET_FREE_SLOT
        )
        cost: int = next(
            requirement.value for requirement in instance.requirements 
            if requirement.requirement.key == Requirement.MANA_COST
        )

        player.resources -= cost
        player.hand.remove(instance.slot)
        target_slot.card = tmpCard
        target_slot.reset()
        target_slot.just_summoned = True

    def resolve_crack(self, instance: ActionInstance):
        
        if(instance.slot is None): raise Exception("Crack Action Instance needs a slot!")

        tmpCard = instance.slot.card
        player = instance.source

        instance.source.resources += tmpCard.resource_capacity
        player.hand.remove(instance.slot)
        player.grave_slots.append(Slot(Slot.GRAVE_SLOT, tmpCard))


    def resolve_action(self, instance: ActionInstance):
        if(instance.action.key == Action.NO_ACT): return

        if(instance.action.key not in self.resolve_map):
            print(f"ActionHandler | No Resolver for {instance.action.key} ignoring for now.")
            return

        self.resolve_map[instance.action.key](instance)