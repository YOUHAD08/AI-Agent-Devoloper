import os

def read_project_file(name: str) -> str:
        with open(name, "r") as f:
            return f.read()

def list_project_files() -> list[str]:
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])
