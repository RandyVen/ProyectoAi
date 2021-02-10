class Node:
    def __init__(self, state, parent, action, value) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.value = value