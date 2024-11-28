from ..core.state import State
from ..core.transition import Transition
from ..core.event import Event
from ..core.workflow import Workflow
from ..core.state import StateRegistry
from ..core.transition import TransitionRegistry
from ..core.event import EventRegistry

def create_states(states_config):
    """Dynamically create states based on the configuration."""
    states = {}
    for state_name, state_config in states_config.items():
        on_enter = state_config.get("on_enter")
        on_exit = state_config.get("on_exit")
        state = State(state_name, on_enter=on_enter, on_exit=on_exit)
        states[state_name] = state
    return states

def create_transitions(transitions_config):
    """Dynamically create transitions based on the configuration."""
    transitions = []
    for transition in transitions_config:
        source, target = transition["source"], transition["target"]
        condition = transition.get("condition")
        action = transition.get("action")
        transition = Transition(source, target, condition=condition, action=action)
        transitions.append(transition)
    return transitions

def create_events(events_config, transitions):
    """Dynamically create events and bind them to transitions."""
    events = {}
    for event_name, event_config in events_config.items():
        event = Event(event_name)
        for transition in event_config["transitions"]:
            # Find the transition object based on source and target
            for t in transitions:
                if t.source == transition["source"] and t.target == transition["target"]:
                    event.add_transition(t)
                    break
        events[event_name] = event
    return events

def load_fsm_from_config(config):
    """Create FSM components from the configuration file."""
    states = create_states(config['states'])
    transitions = create_transitions(config['transitions'])
    events = create_events(config['events'], transitions)
    
    workflow = Workflow(config["name"], {
        "states": list(states.keys()),
        "transitions": [(t.source, t.target, {"condition": t.is_valid, "action": t.execute}) for t in transitions],
        "events": list(events.keys())
    })
    
    return workflow
