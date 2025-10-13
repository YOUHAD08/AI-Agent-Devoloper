"""
README Generator Agent - Practical Approach
"""
import os
from typing import List
import sys

current_file_dir = os.path.dirname(__file__)

from agent_framework import (
    Goal,
    Agent,
    Environment,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    register_tool,
    generate_response
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


@register_tool(tags=["file_operations", "write"])
def write_readme_file(content: str) -> str:
    """Writes the provided content to README.md file."""
    try:
        file_path = os.path.join(current_file_dir, "README.md")
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
    """Main function to run the README generator agent."""
    
    goals = [
        Goal(
            priority=1,
            name="Read Files",
            description="List all Python files and read each one"
        ),
        Goal(
            priority=2,
            name="Generate README",
            description="""Create a professional, modern README with these sections:

                1. Title: Clear, catchy project name (H1)
                2. Badges: Python version, License, Build status
                3. Overview: 2-3 sentences describing the project
                4. Key Features: 5-6 important features with descriptions
                5. Quick Start: Prerequisites, installation steps with code blocks
                6. Usage: Multiple practical examples with code blocks
                7. API Reference: List main functions/classes with descriptions
                8. Project Structure: Brief explanation of file organization
                9. Dependencies: Required packages and their purposes
                10. Contributing: How to contribute
                11. License: License type and link

                Formatting requirements:
                - Use proper markdown headers (# ## ###)
                - Code blocks with language specification (```python, ```bash)
                - Bold text for **important terms**
                - Inline code for `function_names`
                - Line breaks between sections
                - Professional but accessible tone
                - Modern, clean aesthetic

                Make it production-ready and well-organized"""
        ),
        Goal(
            priority=3,
            name="Write to File",
            description="Call write_readme_file with the complete README"
        ),
        Goal(
            priority=4,
            name="Finish",
            description="Call terminate with success message"
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )

    print("=" * 70)
    print("README Generator Agent")
    print("=" * 70)
    print()
    
    agent.run(
        "Generate a professional README by reading files, creating content, writing to README.md, then terminating.",
        max_iterations=40
    )
    
    print()
    print("=" * 70)
    print("Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()