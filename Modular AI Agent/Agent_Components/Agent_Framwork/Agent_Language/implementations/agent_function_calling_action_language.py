from typing import Dict, List, Any
import json
from ....GAME_Components import Action
from ....GAME_Components import Environment
from ....GAME_Components import Goal
from ....GAME_Components import Memory
from ...prompt import Prompt
from ..Interface import AgentLanguage

class AgentFunctionCallingActionLanguage(AgentLanguage):

    def __init__(self):
        super().__init__()

    def format_goals(self, goals: List[Goal]) -> List:
        # Map all goals to a single string that concatenates their description
        # and combine into a single message of type system
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([f"{goal.name}:{sep}{goal.description}{sep}" for goal in goals])
        return [
            {"role": "system", "content": goal_instructions}
        ]

    def format_memory(self, memory: Memory) -> List:
        """Generate response from language model"""
        # Map all environment results to a role:user messages
        # Map all assistant messages to a role:assistant messages
        # Map all user messages to a role:user messages
        items = memory.get_memories()
        mapped_items = []
        for item in items:

            content = item.get("content", None)
            if not content:
                content = json.dumps(item, indent=4)

            if item["type"] == "assistant":
                mapped_items.append({"role": "assistant", "content": content})
            elif item["type"] == "environment":
                mapped_items.append({"role": "assistant", "content": content})
            else:
                mapped_items.append({"role": "user", "content": content})

        return mapped_items

    def format_actions(self, actions: List[Action]) -> List[Dict]:
        """Generate response from language model"""

        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    # Include up to 1024 characters of the description
                    "description": action.description[:1024],
                    "parameters": action.parameters,
                },
            } for action in actions
        ]

        return tools

    def construct_prompt(self,
                         actions: List[Action],
                         goals: List[Goal],
                         memory: Memory) -> Prompt:

        prompt = []
        prompt += self.format_goals(goals)
        prompt += self.format_memory(memory)

        tools = self.format_actions(actions)

        return Prompt(messages=prompt, tools=tools)


    def parse_response(self, response: str) -> dict:
        """Parse LLM response into structured format by extracting the ```json block"""

        try:
            return json.loads(response)

        except Exception as e:
            return {
                "tool": "terminate",
                "args": {"message":response}
            }

