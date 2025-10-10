import json
from typing import Callable
from  ..GAME_Components import ActionRegistry
from  ..GAME_Components import Environment
from  ..GAME_Components import Goal
from  ..GAME_Components import Memory
from  .prompt import Prompt
from  .Agent_Language.Interface import AgentLanguage


class Agent:
    def __init__(self, 
                 goals :list[Goal],
                 agent_language:AgentLanguage,
                 action_registry:ActionRegistry,
                 generate_response:Callable[[Prompt], str],
                 environment:Environment):
        self.goals = goals
        self.agent_language = agent_language
        self.action_registry = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, goals:list[Goal], memory:Memory, action_registry:ActionRegistry) -> Prompt:
        # Construct the prompt based on the agent's goals, memory, and actions
        return self.agent_language.construct_prompt(
            actions=action_registry.list_actions(), 
            goals=goals, 
            memory=memory
        )
    
    def get_action(self, response:str):
        """Parse the response and get the corresponding action."""
        invocation=self.agent_language.parse_response(response)
        action=self.action_registry.get_action(invocation["tool"])
        return action, invocation
    
    def should_terminate(self, response:str) -> bool:
        """Determine if the agent should terminate based on the response."""
        action_def, _ = self.get_action(response)
        return action_def.terminal
    
    def set_current_task(self, task:str, memory:Memory):
        """Set the current task in memory."""
        memory.add_memory({"type":"user", "content":task})

    def update_memory(self, response:str, memory:Memory , result:dict):
        """
        Update the memory with the agent's decision and the environment's response.
        """
        new_memory = [
            {"type":"assistant", "content":response},
            {"type":"user", "content":json.dumps(result)}
        ]
        for mem in new_memory:
            memory.add_memory(mem)

    def prompt_llm_for_action(self, full_prompt:Prompt) -> str:
        """Prompt the LLM to get the next action."""
        response = self.generate_response(full_prompt)
        return response
    

    def run(self, user_input:str, memory=None) -> Memory:
        """Run the agent with the given user input and memory."""
        memory = memory or Memory()
        self.set_current_task(user_input, memory)
        while True:
            
            """construct the prompt with current goals, memory, and actions"""
            full_prompt = self.construct_prompt(self.goals, memory, self.action_registry)
            print("Agent thinking ...")

            """generate response from the agent"""
            response = self.prompt_llm_for_action(full_prompt)
            print("Agent response:", response)

            """Determine which action the agent wants to execute"""
            action, invocation = self.get_action(response)

            """Execute the action in the environment"""
            result = self.environment.execute_action(action, invocation["args"])
            print("Action result:", result)

            """Update the memory with information about what happened"""
            self.update_memory(response, memory, result)

            """Check if the agent wants to terminate"""
            if self.should_terminate(response):
                break
        return memory
