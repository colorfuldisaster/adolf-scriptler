class State(object):
    """A state has an operation, and can be moved into the next state given an input
    """
    @staticmethod
    def run(self, context):
        raise NotImplementedError("Run not immplemented")

    @staticmethod
    def next(self, context):
        raise NotImplementedError("Next not implemented")


class StateMachine(object):
    """Takes a list of inputs to move from state to state using a template method
    """
    def __init__(self, initial_state):
        self.current_state = initial_state

    def run_all(self):
        while True:
            self.current_state.run(self)
            self.current_state = self.current_state.next(self)
            if self.current_state is None:
                break
