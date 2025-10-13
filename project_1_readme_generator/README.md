# README Generator Agent

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)

## Overview
The **README Generator Agent** is a powerful tool designed to automate the creation of professional, modern README files for Python projects. This agent reads through the project's Python files, extracts relevant information, and composes a comprehensive README with key sections essential for any project documentation.

## Key Features
- **Automated File Reading**: Lists and reads all Python files in the project for information gathering.
- **Structured README Creation**: Generates a README with essential sections like Title, Overview, Features, and more.
- **Easy Customization**: Allows for modifications and custom content to suit specific project needs.
- **Markdown Formatting**: Ensures consistent and modern markdown formatting using proper headers and code blocks.
- **Efficient Workflow**: Streamlines the documentation process, saving valuable development time.

## Quick Start
### Prerequisites
- Python 3.8+

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/readme-generator-agent.git

# Navigate to the project directory
cd readme-generator-agent

# Install required packages
pip install -r requirements.txt
```

## Usage
To generate a README file for your project, simply run the following command:
```bash
python readme_generator.py
```

## API Reference
- `read_project_file(name: str) -> str`: Reads and returns the content of a specified project file.
- `list_project_files() -> List[str]`: Lists all Python files in the current project directory.
- `write_readme_file(content: str) -> str`: Writes the provided content to README.md file.
- `terminate(message: str) -> str`: Terminates the agent's execution.

## Project Structure
- **readme_generator.py**: Main script for generating README files.
- **agent_framework**: Contains classes and functions for agent operation and integration.

## Dependencies
- **os**: Used to handle file system operations such as reading and writing files.
- **typing**: Provides type hints for better code readability and maintenance.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
