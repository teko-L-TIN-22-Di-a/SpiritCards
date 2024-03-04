from enum import Enum
import random
from spirit_cards.card_engine.board_constants import BoardConstants
from spirit_cards.card_engine.card import Card
from spirit_cards.card_engine.slot import Slot

class PlayerState(Enum):
    IDLE = 1
    WAIT_FOR_INPUT = 2

class CardPlayer:
    
    deck: list[Card]

    current_deck: list[Card]

    hand: list[Slot]
    battle_slots: list[Slot]
    support_slots: list[Slot]
    grave_slots: list[Slot]

    state: PlayerState = PlayerState.IDLE
    is_dead: bool = False

    def __init__(self, deck: list[Card]):
        self.deck = deck
        self.current_deck = []

        self.hand = []
        self.battle_slots = [Slot() for _ in range(0, BoardConstants.BATTLE_SLOT_COUNT)]
        self.support_slots = [Slot() for _ in range(0, BoardConstants.SUPPORT_SLOT_COUNT)]
        self.grave_slots = []

    def start_game(self) -> None:
        self.current_deck = self.deck.copy()
        random.shuffle(self.current_deck)

        for i in range(0, BoardConstants.HAND_SIZE):
            self.draw_card()

    def draw_card(self) -> None:

        if(len(self.current_deck) <= 0):
            self.is_dead = True
            return

        self.hand.append(Slot(self.current_deck.pop()))