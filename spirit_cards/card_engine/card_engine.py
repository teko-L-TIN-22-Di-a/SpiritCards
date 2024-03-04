from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.round_state import RoundState, RoundStateHandler
from spirit_cards.core.entity import Entity

class CardEngine(Entity):

    board_context: BoardContext

    round_state: RoundStateHandler

    def __init__(self, starting_player, player2):
        self.board_context = BoardContext(starting_player, player2)
        self.round_state = RoundStateHandler(self.board_context)

        self._start_encounter()

    def update(self, delta: float) -> None:
        self.round_state.update()

    def _start_encounter(self) -> None:
        self.board_context.player1.start_game()
        self.board_context.player2.start_game()
        

