from typing import List, Any

from ..core.action import Action
from ..core.environment import Environment
from ..core.goals import Goal
from ..core.memory import Memory
from ..utils.llm import Prompt


class AgentLanguage:
    def __init__(self):
        pass

    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("Subclasses must implement this method")

    def parse_response(self, response: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")
