from Agent_Components.GAME_Components import ActionRegistry
from Agent_Components.GAME_Components import Action
from tools import *

action_registry = ActionRegistry()
action_registry.register(Action(
    name="list_project_files",
    function=list_project_files,
    description="Lists all files in the project.",
    parameters={},
    terminal=False
))
action_registry.register(Action(
    name="read_project_file",
    function=read_project_file,
    description="Reads a file from the project.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    },
    terminal=False
    ))
action_registry.register(Action(
    name="terminate",
    function=lambda message: f"{message}\nTerminating...",
    description="Terminates the session and prints the message to the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": []
    },
    terminal=True
))
