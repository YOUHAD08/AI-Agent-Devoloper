import os

def list_files() -> list:
    """Lists all files in the current directory."""
    return os.listdir('.')

def read_file(file_path: str) -> str:
    """Reads the content of a specified file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    with open(file_path, 'r') as file:
        return file.read()
    
def search_in_file(file_path: str, search_term: str) -> list:
    """Searches for a term in the specified file and returns lines containing the term."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    results = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if search_term in line:
                results.append((line_number, line.strip()))
    return results