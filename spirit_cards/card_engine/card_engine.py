from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.round_context import RoundContext
from spirit_cards.card_engine.round_state import RoundState, RoundStateHandler


class CardEngine:
    
    _board_context: BoardContext
    _round_context: RoundContext

    _round_state: RoundStateHandler

    def __init__(self, starting_player, player2):
        self._board_context = BoardContext()
        self._round_context = RoundContext(starting_player, player2)
        self._round_state = RoundStateHandler(self._round_context, self._board_context)

    def update(self) -> None:
        self._round_state.update()
        

