

from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.card import Card
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.round_state import RoundState
from spirit_cards.card_engine.slot import Slot

class Actions:

    ALL_PHASES = [
        RoundState.REFRESH_PHASE,
        RoundState.MAIN_PHASE,
        RoundState.BATTLE_PHASE,
        RoundState.MAIN_PHASE_2,
        RoundState.END_PHASE
    ]

    def get_base():
        return [
            Actions.get_summon(),
            Actions.get_attack(),
            Actions.get_crack(),
        ]

    def get_summon():
        return Action(
            Action.SUMMON, 
            phase_availability = [RoundState.MAIN_PHASE, RoundState.MAIN_PHASE_2],
            placement_requirements = [Slot.HAND_SLOT],
            requirements = [Requirement(Requirement.MANA_COST), Requirement(Requirement.TARGET_FREE_SLOT)]
        )

    def get_attack():
        return Action(
            Action.ATTACK, 
            phase_availability = [RoundState.BATTLE_PHASE],
            placement_requirements = [Slot.BATTLE_SLOT],
            requirements = [Requirement(Requirement.BATTLE_TARGET)]
        )
    
    def get_crack():
        return Action(
            Action.CRACK,
            phase_availability = Actions.ALL_PHASES,
            placement_requirements = [Slot.HAND_SLOT],
            only_playing = False,
            requirements = [],
            resolve_instantly = True
        )

def get_test_card():
    return Card(Actions.get_base(), AssetMap.TEST_CARD,
                health=2, attack=2,
                resource_capacity=2,
                cost= 2)

def get_test_card2():
    return Card(Actions.get_base(), AssetMap.TEST_CARD2,
                health=2, attack=2,
                resource_capacity=2,
                cost= 2)

def get_test_card3():
    return Card(Actions.get_base(), AssetMap.TEST_CARD3,
                health=2, attack=2,
                resource_capacity=2,
                cost= 2)

def get_test_card4():
    return Card(Actions.get_base(), AssetMap.TEST_CARD4,
                health=2, attack=2,
                resource_capacity=2,
                cost= 2)
