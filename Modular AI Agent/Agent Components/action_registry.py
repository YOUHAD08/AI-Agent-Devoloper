from action import Action


class ActionRegistry:
    def __init__(self):
        self._actions = {}

    def register_action(self, action : Action):
        """Registers a new action with the given name and function."""
        if action.name in self._actions:
            raise ValueError(f"Action '{action.name}' is already registered.")
        self._actions[action.name] = action

    def get_action(self, name: str) -> Action | None:
        """Retrieves the action function associated with the given name."""
        if name not in self._actions:
            raise ValueError(f"Action '{name}' is not registered.")
        return self._actions[name]

    def list_actions(self):
        """Lists all registered action names."""
        return list(self._actions.values())