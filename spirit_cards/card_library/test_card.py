

from spirit_cards.asset_map import AssetMap
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.card import Card
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.round_state import RoundState

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
            [RoundState.MAIN_PHASE, RoundState.MAIN_PHASE_2], 
            [Requirement(Requirement.MANA_COST), Requirement(Requirement.TARGET_SLOT)]
        )

    def get_attack():
        return Action(
            Action.ATTACK, 
            [RoundState.BATTLE_PHASE], 
            [Requirement(Requirement.BATTLE_TARGET)]
        )
    
    def get_crack():
        return Action(
            Action.CRACK,
            Actions.ALL_PHASES,
            []
        )

def get_test_card():
    return Card(Actions.get_base(), AssetMap.TEST_CARD, 2, 2)

def get_test_card2():
    return Card(Actions.get_base(), AssetMap.TEST_CARD2, 2, 2)

def get_test_card3():
    return Card(Actions.get_base(), AssetMap.TEST_CARD3, 2, 2)

def get_test_card4():
    return Card(Actions.get_base(), AssetMap.TEST_CARD4, 2, 2)
