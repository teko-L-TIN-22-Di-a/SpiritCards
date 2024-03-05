
from spirit_cards.card_engine.action import Action, Actions
from spirit_cards.card_engine.action_instance import ActionInstance
from spirit_cards.card_engine.board_context import BoardContext
from spirit_cards.card_engine.card_player import CardPlayer, PlayerState
from spirit_cards.card_engine.requirement import Requirement
from spirit_cards.card_engine.slot import Slot
from spirit_cards.core.state_machine.state_machine import State, StateMachine

class RoundStateHandler(StateMachine):

    def __init__(self, board_context: BoardContext):

        states = {
            RoundState.REFRESH_PHASE: RefreshPhase(board_context),
            RoundState.MAIN_PHASE: MainPhase(board_context),
            RoundState.BATTLE_PHASE: BattlePhase(board_context),
            RoundState.MAIN_PHASE_2: MainPhase2(board_context),
            RoundState.END_PHASE: EndPhase(board_context),
        }

        super().__init__(states, RoundState.REFRESH_PHASE)

    def buffer_action(self, action: ActionInstance) -> None:
        current_state: RoundState = self.current_state
        return current_state.buffer_action(action)

    def get_legal_actions(self, slot: Slot) -> list[Action]:
        current_state: RoundState = self.current_state
        return current_state.get_legal_actions(slot)
    
    def get_actions(self, player: CardPlayer) -> list[Action]:
        if(player.state == PlayerState.IDLE):
            return []

        current_state: RoundState = self.current_state
        return current_state.get_actions(player)

class RoundState(State):
    
    REFRESH_PHASE = "refresh_phase"
    MAIN_PHASE = "main_phase"
    BATTLE_PHASE = "battle_phase"
    MAIN_PHASE_2 = "main_phase_2"
    END_PHASE = "end_phase"

    current_phase: str
    next_phase: str

    buffered_action: ActionInstance = None
    action_stack: list[ActionInstance]

    board_context: BoardContext

    def __init__(self, board_context: BoardContext, current_phase: str, next_phase_key):
        self.board_context = board_context
        self.action_stack = []
        self.current_phase = current_phase
        self.next_phase = next_phase_key

    def enter(self, msg: dict) -> None:
        self.action_stack = []

    def buffer_action(self, action: ActionInstance):

        if(action.action.key == Action.CANCEL_ACTION):
            self.buffered_action = None

        self.buffered_action = action

    def get_legal_actions(self, slot: Slot) -> list[Action]:
        if(slot.card is None):
            return []
        
        actions: list[Action] = []

        for action in slot.card.actions:
            if(self.current_phase in action.availability):
                actions.append(action)

        return actions
    
    def get_actions(self, player: CardPlayer) -> list[Action]:    
        actions = []

        if(len(self.action_stack) <= 0 and self.buffered_action is None):
            actions.append(Action(Action.NEXT_PHASE))
        
        if(len(self.action_stack) > 0 and self.buffered_action is None):
            actions.append(Action(Action.NO_ACT))

        return actions

    def process_effects(self):
        # Go through filtered list of cards on board and execute effects.
        pass

    def process_actions(self):
        self.process_requirement()
        self.process_reaction()
        self.process_action()

    def process_requirement(self):
        if(self.buffered_action is None):
            return
        
        if(self.buffered_action.is_complete()):
            self.resolve_requirement_stack()
            self.action_stack.append(self.buffered_action)
            self.buffered_action = None

        # TODO Implement way of resolving single requirements

    def process_action(self):
        if(len(self.action_stack) > 0):
            return
        
        self.board_context.player.state = PlayerState.WAIT_FOR_INPUT
        self.board_context.opponent.state = PlayerState.IDLE

        # TODO implement going through all slots / cards and highlighting them / checking them for actions

    def process_reaction(self):
        if(len(self.action_stack) <= 0):
            return
        
        top_element = self.action_stack[-1]
        if(top_element.action.key == Action.NO_ACT):
            self.resolve_action_stack()

        if(top_element.source == self.board_context.opponent or
           top_element.source is None):
            self.board_context.player.state = PlayerState.WAIT_FOR_INPUT
            self.board_context.opponent.state = PlayerState.IDLE
        elif(top_element.source == self.board_context.player):
            self.board_context.player.state = PlayerState.IDLE
            self.board_context.opponent.state = PlayerState.WAIT_FOR_INPUT

        # TODO same as with action but filtered towards only reaction stuff
    
    def resolve_requirement_stack(self):
        pass

    def resolve_action_stack(self):

        while(len(self.action_stack) > 0):
            
            current_action = self.action_stack.pop()

            if(current_action.action.key == Action.NEXT_PHASE):
                self.transition_to(self.next_phase)

    def swap_players(self):
        player = self.board_context.player
        self.board_context.player = self.board_context.opponent
        self.board_context.opponent = player
        

class RefreshPhase(RoundState):

    def __init__(self, board_context: BoardContext):
        super().__init__(board_context, RoundState.REFRESH_PHASE, RoundState.MAIN_PHASE)

    def enter(self, msg: dict) -> None:

        if(self.board_context.round_count != 1):
            self.board_context.player.draw_card()

        self.action_stack.append(ActionInstance(Actions[Action.NEXT_PHASE], None, None))
        self.action_stack.append(ActionInstance(Actions[Action.ON_REFRESH], None, None))

    def update(self) -> None:
        self.process_actions()

class MainPhase(RoundState):

    def __init__(self, board_context: BoardContext):
        super().__init__(board_context, RoundState.MAIN_PHASE, RoundState.BATTLE_PHASE)
    
    def update(self) -> None:
        self.process_actions()

class BattlePhase(RoundState):
    
    def __init__(self, board_context: BoardContext):
        super().__init__(board_context, RoundState.BATTLE_PHASE, RoundState.MAIN_PHASE_2)

    def update(self) -> None:
        self.process_actions()

class MainPhase2(RoundState):
    
    def __init__(self, board_context: BoardContext):
        super().__init__(board_context, RoundState.MAIN_PHASE_2, RoundState.END_PHASE)

    def update(self) -> None:
        self.process_actions()

class EndPhase(RoundState):
    
    def __init__(self, board_context: BoardContext):
        super().__init__(board_context, RoundState.END_PHASE, RoundState.REFRESH_PHASE)

    def enter(self, msg: dict) -> None:
        self.action_stack.append(ActionInstance(Actions[Action.NEXT_PHASE], None, None))
        self.action_stack.append(ActionInstance(Actions[Action.ON_END], None, None))

    def update(self) -> None:
        self.process_actions()

    def exit(self) -> None:
        self.swap_players()
        self.board_context.round_count += 1