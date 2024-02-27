from typing import Callable


class State:

    transition_to: Callable[[str, dict | None], None]
    transition_back: Callable[[dict | None], None]

    def update(self) -> None:
        pass

    def enter(self, msg: dict) -> None:
        pass

    def exit(self) -> None:
        pass

class StateMachine:

    MAX_STACK_SIZE = 5

    _states: dict[str, State]

    _state_stack: list[State]
    current_state: State = None

    def __init__(self, states: dict[str, State], inital_state: str):
        self._states = states

        for state in states:
            states[state].transition_back = self.transition_back
            states[state].transition_to = self.transition_to

        self.transition_to(inital_state)

    def update(self) -> None:
        if(self.current_state is not None):
            self.current_state.update()

    def transition_to(self, state_key: str, msg: dict = {}) -> None:
        
        if(state_key not in self._states):
            raise Exception(f"State with {state_key} doesn't exist!")

        if(self.current_state is not None):
            self.current_state.exit()
            
            self._state_stack.append(self.current_state)

            if(len(self._state_stack) > StateMachine.MAX_STACK_SIZE):
                self.current_state = self.current_state[1:]
        
        self.current_state = self._states[state_key]
        self.current_state.enter(msg)

    def transition_back(self, msg: dict = {}) -> None:
        
        if(len(self._state_stack) <= 0):
            raise Exception("StateStack empty no states to go back to!")
        
        self.current_state.exit()

        self.current_state = self._state_stack.pop()
        self.current_state.enter(msg)
