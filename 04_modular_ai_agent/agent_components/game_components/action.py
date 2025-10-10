from dataclasses import dataclass
from typing import Callable, Any, Dict

@dataclass
class Action:
    name: str
    function: Callable[..., Any]
    description: str
    parameters: Dict
    terminal: bool = False

    def execute(self, **args) -> Any:
        """Executes the action function with the provided arguments."""
        return self.function(**args)