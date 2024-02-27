
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.round_context import RoundContext
from spirit_cards.core.state_machine.state_machine import State, StateMachine

class RoundState(State):
    
    REFRESH_PHASE = "refresh_phase"
    MAIN_PHASE = "main_phase"
    BATTLE_PHASE = "battle_phase"
    MAIN_PHASE_2 = "main_phase_2"
    END_PHASE = "end_phase"

    action_stack: list[Action]

    round_context: RoundContext
    board_context: BoardContext

    def __init__(self, round_context: RoundContext, board_context: BoardContext):
        self.round_context = round_context
        self.board_context = board_context

    def process_effects(self):
        # Go through filtered list of cards on board and execute effects.
        pass

    def request_action(self):
        if(self.action_stack.count() > 0):
            return
        
        # Get Action
        pass

    def request_reaction(self):
        if(self.action_stack.count() <= 0):
            return
        
        if(self.action_stack[-1].key == Action.NO_ACT):
            self.resolve_action_stack()

        # Get Reaction
        
    def resolve_action_stack(self):
        pass
        


class RoundStateHandler(StateMachine):

    def __init__(self, round_context: RoundContext, board_context: BoardContext):

        states = {
            RoundState.REFRESH_PHASE: RefreshPhase(round_context, board_context),
            RoundState.MAIN_PHASE: MainPhase(round_context, board_context),
            RoundState.BATTLE_PHASE: BattlePhase(round_context, board_context),
            RoundState.MAIN_PHASE_2: MainPhase2(round_context, board_context),
            RoundState.END_PHASE: EndPhase(round_context, board_context),
        }

        super().__init__(states, RoundState.REFRESH_PHASE)

class RefreshPhase(RoundState):
    
    def update(self) -> None:
        pass

class MainPhase(RoundState):
    
    def update(self) -> None:
        pass

class BattlePhase(RoundState):
    
    def update(self) -> None:
        pass

class MainPhase2(RoundState):
    
    def update(self) -> None:
        pass

class EndPhase(RoundState):
    
    def update(self) -> None:
        pass