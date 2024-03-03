from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.round_context import RoundContext
from spirit_cards.card_engine.round_state import RoundState, RoundStateHandler
from spirit_cards.core.entity import Entity


class CardEngine(Entity):
    
    TAG = "card_engine"

    board_context: BoardContext
    round_context: RoundContext

    round_state: RoundStateHandler

    def __init__(self, starting_player, player2):
        self.board_context = BoardContext()
        self.round_context = RoundContext(starting_player, player2)
        self.round_state = RoundStateHandler(self.round_context, self.board_context)

    def update(self, delta: float) -> None:
        self.round_state.update()
        

