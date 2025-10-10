from typing import Dict, List, Any
import json
from ....game_components import Action
from ....game_components import Goal
from ....game_components import Memory
from ..Interface import AgentLanguage
from ...prompt import Prompt

class AgentJsonActionLanguage(AgentLanguage):
    action_format = """
      <Stop and think step by step. Insert your thoughts here.>

      action
      {
          "tool": "tool_name",
          "args": {...fill in arguments...}
      }
    """

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
    def format_goals(self, goals: List[Goal]) -> List:
        # Map all goals to a single string that concatenates their description
        # and combine into a single message of type system
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([f"{goal.name}:{sep}{goal.description}{sep}" for goal in goals])
        return [
            {"role": "system", "content": goal_instructions}
        ]

    def format_actions(self, actions: List[Action]) -> List:
        # Convert actions to a description the LLM can understand
        action_descriptions = [
            {
                "name": action.name,
                "description": action.description,
                "args": action.parameters
            } 
            for action in actions
        ]
        
        return [{
            "role": "system",
            "content": f"""
Available Tools: {json.dumps(action_descriptions, indent=4)}

{self.action_format}
"""
        }]
    
    def construct_prompt(self,
                         actions: List[Action],
                         goals: List[Goal],
                         memory: Memory) -> Prompt:

        prompt = []
        goal_message = self.format_goals(goals)[0]['content']
        tools_message = self.format_actions(actions)[0]['content']
        prompt.append({"role": "system", "content": goal_message + "\n\n" + tools_message})
        prompt += self.format_memory(memory)


        return Prompt(messages=prompt)

    def parse_response(self, response: str) -> dict:
        """Extract and parse the action block"""
        try:
            start_marker = "action"
            end_marker = ""
            
            stripped_response = response.strip()
            start_index = stripped_response.find(start_marker)
            end_index = stripped_response.rfind(end_marker)
            json_str = stripped_response[
                start_index + len(start_marker):end_index
            ].strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"Failed to parse response: {str(e)}")
            raise e