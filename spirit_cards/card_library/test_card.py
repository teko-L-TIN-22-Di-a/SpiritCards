

from spirit_cards.asset_map import TEST_CARD
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.card import Card
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.round_state import RoundState


def get_test_card():

    card = Card([
        Action(
            Action.SUMMON, 
            [RoundState.MAIN_PHASE, RoundState.MAIN_PHASE_2], 
            [Requirement(Requirement.MANA_COST), Requirement(Requirement.TARGET_SLOT)]
            ),
        Action(
            Action.ATTACK, 
            [RoundState.BATTLE_PHASE], 
            [Requirement(Requirement.BATTLE_TARGET)]
            )
    ], TEST_CARD, 2, 2)

    return card
