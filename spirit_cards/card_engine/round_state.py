
from spirit_cards.card_engine.action import Action
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.round_context import RoundContext
from spirit_cards.core.state_machine.state_machine import State, StateMachine

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

class RoundState(State):
    
    REFRESH_PHASE = "refresh_phase"
    MAIN_PHASE = "main_phase"
    BATTLE_PHASE = "battle_phase"
    MAIN_PHASE_2 = "main_phase_2"
    END_PHASE = "end_phase"

    next_phase = None

    buffered_action: Action = None
    action_stack: list[Action] = []
    requirements_stack: list[Requirement] = []

    round_context: RoundContext
    board_context: BoardContext

    def __init__(self, round_context: RoundContext, board_context: BoardContext):
        self.round_context = round_context
        self.board_context = board_context

    def enter(self, msg: dict) -> None:
        self.action_stack = []

    def process_effects(self):
        # Go through filtered list of cards on board and execute effects.
        pass

    def process_actions(self, next_phase: str):
        self.process_requirement()
        self.process_reaction(next_phase)
        self.process_action()

    def process_requirement(self):
        if(self.buffered_action is None):
            return
        
        if(len(self.requirements_stack) == len(self.buffered_action.requirements)):
            self.resolve_requirement_stack()
            self.action_stack.append(self.buffered_action)
            self.buffered_action = None

    def process_action(self):
        if(len(self.action_stack) > 0):
            return
        
        # TODO implement going through all slots / cards and highlighting them / checking them for actions
        pass

    def process_reaction(self, next_phase: str):
        if(len(self.action_stack) <= 0):
            return
        
        top_element = self.action_stack[-1]
        if(top_element.key == Action.NO_ACT):
            self.resolve_action_stack(next_phase)

        # TODO same as with action but filtered towards only reaction stuff
    
    def resolve_requirement_stack(self):
        pass

    def resolve_action_stack(self, next_phase: str):
        current_action = self.action_stack.pop()
        
        while(current_action is not None):

            if(current_action.key == Action.NEXT_PHASE):
                self.transition_to(next_phase)

    def swap_players(self):
        player = self.round_context.player
        self.round_context.player = self.round_context.opponent
        self.round_context.opponent = player
        

class RefreshPhase(RoundState):

    def enter(self, msg: dict) -> None:
        self.action_stack.append(Action(Action.ON_REFRESH, source=Action.SYSTEM_SOURCE))

    def update(self) -> None:
        self.process_actions(RoundState.MAIN_PHASE)

class MainPhase(RoundState):
    
    def update(self) -> None:
        self.process_actions(RoundState.BATTLE_PHASE)

class BattlePhase(RoundState):
    
    def update(self) -> None:
        self.process_actions(RoundState.MAIN_PHASE_2)

class MainPhase2(RoundState):
    
    def update(self) -> None:
        self.process_actions(RoundState.END_PHASE)

class EndPhase(RoundState):
    
    def enter(self, msg: dict) -> None:
        self.action_stack.append(Action(Action.ON_END, source=Action.SYSTEM_SOURCE))

    def update(self) -> None:
        self.process_actions(RoundState.REFRESH_PHASE)

    def exit(self) -> None:
        self.swap_players()
        self.round_context.round_count += 1