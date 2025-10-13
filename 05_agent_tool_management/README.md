# Agent Framework - GAME Architecture

![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Overview

The **Agent Framework** is a comprehensive, modular Python framework for building intelligent autonomous agents using the **GAME** (Goals, Actions, Memory, Environment) architecture. It provides a flexible foundation for creating goal-oriented agents that can interact with their environment through registered tools and maintain context through persistent memory.

## Key Features

- **GAME Architecture**: Goals-driven execution with Actions, Memory, and Environment components
- **Tool Registration System**: Decorator-based tool registration with automatic schema inference
- **Function Calling Interface**: Seamless integration with OpenAI's function calling API
- **Flexible Tool Management**: Registry system with tag-based tool filtering and selection
- **Memory Management**: Conversational memory system for maintaining agent context
- **Language Abstraction**: Pluggable language interface for different LLM communication styles
- **Action Execution**: Type-safe action execution with error handling
- **Extensible Design**: Easy to extend with custom actions, memory types, and language implementations

## Architecture

### Core Components

- **Agent**: Orchestrates the GAME loop and manages goal-oriented execution
- **Environment**: Executes actions safely with result formatting and error handling
- **ActionRegistry**: Manages available actions/tools with filtering capabilities
- **Memory**: Maintains conversation history and agent context
- **Goals**: Defines agent objectives with priorities and descriptions

### Language Layer

- **AgentLanguage**: Base class for LLM communication strategies
- **AgentFunctionCallingActionLanguage**: Implements OpenAI function calling protocol

### Tool System

- **Tool Registry**: Decorator-based registration with automatic metadata extraction
- **PythonActionRegistry**: Python-specific action registry with tag filtering
- **Parameter Schema Generation**: Automatic JSON schema inference from function signatures

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM integration)

### Installation

```bash
# Clone or navigate to the framework directory
cd 05_agent_tool_management

# Install as development package
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Usage

### Creating a Simple Agent

```python
from agent_framework import (
    Agent,
    Goal,
    Environment,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    register_tool,
    generate_response
)

# Step 1: Register your tools
@register_tool(tags=["example"], terminal=False)
def my_tool(param1: str) -> str:
    """Description of my tool."""
    return f"Result: {param1}"

# Step 2: Define agent goals
goals = [
    Goal(priority=1, name="Do Something", description="Description here"),
    Goal(priority=2, name="Finish", description="Complete execution")
]

# Step 3: Create and run agent
agent = Agent(
    goals=goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=PythonActionRegistry(),
    generate_response=generate_response,
    environment=Environment()
)

memory = agent.run("Your task here", max_iterations=50)
```

### Registering Tools

```python
@register_tool(
    tool_name="custom_name",
    description="What this tool does",
    terminal=False,
    tags=["category", "subcategory"]
)
def my_function(param1: str, param2: int) -> dict:
    """Function docstring serves as default description."""
    return {"result": "value"}
```

## Project Structure

```
05_agent_tool_management/
├── agent_framework/
│   ├── __init__.py
│   ├── core/
│   │   ├── action.py          # Action and ActionRegistry classes
│   │   ├── agent.py           # Main Agent class
│   │   ├── environment.py      # Environment execution engine
│   │   ├── goals.py           # Goal dataclass
│   │   ├── memory.py          # Memory management
│   │   └── __init__.py
│   ├── language/
│   │   ├── base.py            # AgentLanguage base class
│   │   ├── function_calling.py # OpenAI function calling implementation
│   │   └── __init__.py
│   ├── tools/
│   │   ├── registry.py        # Tool registration system
│   │   ├── python_registry.py # Python-specific registry
│   │   └── __init__.py
│   ├── utils/
│   │   ├── llm.py             # LLM utilities and Prompt class
│   │   └── __init__.py
│   └── __pycache__/
├── agent_framework.egg-info/  # Package metadata (auto-generated)
├── README.md
├── requirements.txt
├── setup.py
└── .gitignore
```

## API Reference

### Agent Class

```python
Agent(goals, agent_language, action_registry, generate_response, environment)
```

**Methods:**

- `run(user_input, memory=None, max_iterations=50)` - Execute agent loop
- `construct_prompt(goals, memory, actions)` - Build LLM prompt
- `get_action(response)` - Parse LLM response into action
- `should_terminate(response)` - Check if execution should stop
- `update_memory(memory, response, result)` - Update agent memory

### Environment Class

```python
Environment()
```

**Methods:**

- `execute_action(action, args)` - Execute action with arguments
- `format_result(result)` - Format execution result with metadata

### Tool Registration

```python
@register_tool(tool_name, description, parameters_override, terminal, tags)
def your_function(**args):
    pass
```

### Memory Class

```python
Memory()
```

**Methods:**

- `add_memory(memory)` - Add memory item
- `get_memories(limit=None)` - Retrieve memory items
- `copy_without_system_memories()` - Get filtered memory copy

## Dependencies

- **litellm>=1.0.0** - Unified LLM API interface
- **openai>=1.0.0** - OpenAI API client

## Development

### Running Tests

```bash
pytest tests/
pytest --cov=agent_framework tests/
```

### Code Quality

```bash
black agent_framework/
flake8 agent_framework/
pylint agent_framework/
```

## Advanced Usage

### Custom Language Implementation

```python
from agent_framework import AgentLanguage

class CustomLanguage(AgentLanguage):
    def construct_prompt(self, actions, goals, memory):
        # Your implementation
        pass

    def parse_response(self, response):
        # Your implementation
        pass
```

### Filtering Tools by Tags

```python
registry = PythonActionRegistry(
    tags=["file_operations"],
    tool_names=["read_file", "write_file"]
)
```

## Error Handling

The framework provides robust error handling:

- **Tool Execution**: Errors are caught and formatted with traceback information
- **Memory Management**: Safely handles memory operations with filtering
- **LLM Integration**: Graceful fallback for function calling failures

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created as part of AI Agent development course materials.

## Support

For issues, questions, or suggestions, please open an issue on the repository.
