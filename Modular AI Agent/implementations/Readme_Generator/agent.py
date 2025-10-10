import os
import sys
# Get the directory where THIS file (agent.py) is located
current_file_dir = os.path.dirname(__file__)
# This gives: "C:\...\Modular AI Agent\implementations\Readme_Generator"

# Go up TWO levels (..\.. means "parent's parent")
project_root = os.path.abspath(os.path.join(current_file_dir, "../.."))
# This gives: "C:\...\Modular AI Agent"

# Tell Python: "Look for modules starting from project_root"
sys.path.insert(0, project_root)

from Agent_Components.Agent_Framwork.Agent_Language.implementations import AgentFunctionCallingActionLanguage
from Agent_Components.GAME_Components import Environment
from Agent_Components.Agent_Framwork import Agent
from goals import goals
from registry import action_registry 
from Agent_Components.Agent_Framwork import generate_response


agent_language = AgentFunctionCallingActionLanguage()
environment = Environment()
agent = Agent(goals, agent_language, action_registry, generate_response, environment)
if __name__ == "__main__":
    # Run the agent with user input
    user_input = "Write a README for this project."
    final_memory = agent.run(user_input)
    
    # Print the final memory
    print(final_memory.get_memories())
