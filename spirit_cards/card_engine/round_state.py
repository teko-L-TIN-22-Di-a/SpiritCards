
from spirit_cards.core.state_machine.state_machine import State, StateMachine

REFRESH_PHASE = "refresh_phase"
MAIN_PHASE = "main_phase"
BATTLE_PHASE = "battle_phase"
MAIN_PHASE_2 = "main_phase_2"
END_PHASE = "end_phase"

class RoundState(State):
    pass

class RoundStateMachine(StateMachine):

    def __init__(self):

        states = {
            REFRESH_PHASE: RefreshPhase(),
            MAIN_PHASE: MainPhase(),
            BATTLE_PHASE: BattlePhase(),
            MAIN_PHASE_2: MainPhase2(),
            END_PHASE: EndPhase(),
        }

        super().__init__(states, REFRESH_PHASE)

class RefreshPhase(RoundState):
    pass

class MainPhase(RoundState):
    pass

class BattlePhase(RoundState):
    pass

class MainPhase2(RoundState):
    pass

class EndPhase(RoundState):
    pass