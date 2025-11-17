"""
Enhanced README Generator - With self-prompting analysis
"""
import os
import sys
from typing import List

current_file_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_file_dir)
sys.path.insert(0, parent_dir)

from agent_framework import (
    Goal,
    Agent,
    Environment,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    register_tool,
    generate_response,
    ActionContext
)

@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Reads and returns the content of a specified project file."""
    try:
        file_path = os.path.join(current_file_dir, name)
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{name}' not found."
    except Exception as e:
        return f"Error reading file '{name}': {str(e)}"


@register_tool(tags=["file_operations", "list"])
def list_project_files() -> List[str]:
    """Lists all Python files in the current project directory."""
    try:
        python_files = sorted([
            file for file in os.listdir(current_file_dir)
            if file.endswith(".py")
        ])
        return python_files
    except Exception as e:
        return [f"Error listing files: {str(e)}"]


@register_tool(tags=["analysis", "code"])
def analyze_code_structure(action_context: ActionContext, code: str) -> dict:
    """
    Analyze code structure using LLM.
    This is a SPECIALIZED self-prompting tool.
    """
    from agent_framework.tools.llm_tools import prompt_llm_for_json
    
    schema = {
        "type": "object",
        "properties": {
            "purpose": {"type": "string"},
            "key_components": {
                "type": "array",
                "items": {"type": "string"}
            },
            "dependencies": {
                "type": "array",
                "items": {"type": "string"}
            },
            "complexity": {"type": "string", "enum": ["simple", "moderate", "complex"]},
            "main_functions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"}
                    }
                }
            }
        }
    }
    
    prompt = f"""
Analyze this Python code and extract:
- The overall purpose of the code
- Key components and classes
- External dependencies used
- Complexity level (simple/moderate/complex)
- Main functions with their descriptions

Code:
{code}
"""
    
    return prompt_llm_for_json(action_context, schema, prompt)


@register_tool(tags=["file_operations", "write"])
def write_readme_file(content: str) -> str:
    """Writes the provided content to README.md file."""
    try:
        file_path = os.path.join(current_file_dir,"generated_readme", "README.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n[SUCCESS] README.md written to {file_path}\n")
        return f"README.md successfully written"
    except Exception as e:
        print(f"\n[ERROR] Failed to write README.md: {str(e)}\n")
        return f"Failed to write README.md"


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return f"{message}"


def main():
    """Main function to run the enhanced README generator agent."""
    
    goals = [
        Goal(
            priority=1,
            name="Read Files",
            description="List all Python files and read each one"
        ),
        Goal(
            priority=2,
            name="Analyze Code",
            description="Use analyze_code_structure to understand each file's purpose and components"
        ),
        Goal(
            priority=3,
            name="Generate README",
            description="""Create a professional README with these sections:
                1. Title and Overview
                2. Key Features (based on code analysis)
                3. Project Structure
                4. Installation
                5. Usage Examples
                6. API Reference (based on analyzed functions)
                7. Contributing
                8. License"""
        ),
        Goal(
            priority=4,
            name="Write to File",
            description="Call write_readme_file with the complete README"
        ),
        Goal(
            priority=5,
            name="Finish",
            description="Call terminate with success message"
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(tags=["file_operations", "analysis", "system", "llm"]),
        generate_response=generate_response,
        environment=Environment()
    )

    print("=" * 70)
    print("Enhanced README Generator Agent (With Code Analysis)")
    print("=" * 70)
    print()
    
    agent.run(
        "Generate a professional README by reading files, analyzing code structure, creating content, writing to README.md, then terminating.",
        max_iterations=40
    )
    
    print()
    print("=" * 70)
    print("Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()