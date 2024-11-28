# State Registry to manage dynamically created state classes
class StateRegistry:
    """Manages all dynamically created state classes."""
    _states = {}

    @classmethod
    def register(cls, name, on_enter=None, on_exit=None):
        def create_state_class(name, on_enter=None, on_exit=None):
            """Dynamically creates a state class with custom behavior."""
            def default_enter(self):
                print(f"Entering {name}")

            def default_exit(self):
                print(f"Exiting {name}")

            methods = {
                "enter": on_enter or default_enter,
                "exit": on_exit or default_exit,
                "__repr__": lambda self: f"<State: {name}>",
            }
            return type(name, (object,), methods)
        
        if name in cls._states:
            raise ValueError(f"State '{name}' is already registered.")
        state_class = create_state_class(name, on_enter, on_exit)
        cls._states[name] = state_class
        return state_class

    @classmethod
    def get(cls, name):
        """Retrieve a registered state class by name."""
        if name not in cls._states:
            raise ValueError(f"State '{name}' is not registered.")
        return cls._states[name]


# User-facing State API
class State:
    """User API for creating and using states."""
    def __init__(self, name, on_enter=None, on_exit=None):
        self.name = name
        self._state_class = StateRegistry.register(name, on_enter, on_exit)
        self._state_instance = self._state_class()

    def __getattr__(self, attr):
        """Delegate attribute access to the dynamically created state instance."""
        return getattr(self._state_instance, attr)

    def __repr__(self):
        return repr(self._state_instance)
