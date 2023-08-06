class StateMachine(object):
    """
    StateMachine model interpreter.
    """
    def __init__(self, model):
        self.model = model

        self.current_state = None

        # First state is initial
        self.initial_state = model.states[0]

        # We are in the initial state at the beginning
        self.set_state(self.initial_state)

    def set_state(self, state):
        if self.current_state is None or state is not self.current_state:
            # Trigger state actions
            for action in state.actions:
                group_finder = [idx for idx,objx in enumerate(self.model.commandGroupBlocks) if action == objx]
                if len(group_finder) > 0:
                    for grpCommand in self.model.commandGroupBlocks[group_finder[0]].groupCommands:
                        print("Executing group action ", grpCommand.name)                                            
                else:
                    print("Executing individual action ", action.name)
            print("Transition to state ", state.name)
            self.current_state = state

    def event(self, event):        
        for transition in self.current_state.transitions:
            if transition.event is event:
                self.set_state(transition.to_state)
                return

    def print_menu(self):
        print("Current state: ", self.current_state.name)
        print("Choose event:")
        for idx, event in enumerate(self.model.events):
            print(idx + 1, '-', event.name, event.code)       
        print('q - quit')

    def interpret(self):
        """
        Main interpreter loop.
        """
        self.print_menu()
        while True:
            try:
                event = input()
                if event == 'q':
                    return
                event = int(event)
                event = self.model.events[event - 1]
            except Exception:
                print('Invalid input')

            self.event(event)
            self.print_menu()


