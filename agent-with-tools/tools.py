import os
from typing import List, Dict

def list_files_and_folders(directory: str="C:\\") -> List[str]:
    """List files and folders in the specified directory. Defaults to C:\\ if no directory is provided."""

    if not os.path.isdir(directory):
        return {"error": f"Invalid directory : {directory} . call print_current_working_directory to inform the user of his current working directory,"}
    
    return os.listdir(directory)

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return {"Error" : f"{file_name} not found. call list_files_and_folders to list the files and folders in the current working directory "}
    except Exception as e:
        return {"Error":str(e)}
    
def print_current_working_directory():
    """Print the current working directory."""
    return os.getcwd()

def folder_or_file(folder_or_file_path: str) -> str:
    """Check if the given path is a folder, a file, or does not exist."""
    if os.path.isdir(folder_or_file_path):
        return "folder"
    elif os.path.isfile(folder_or_file_path):
        return "file"
    else:
        return {"Error" : f"{folder_or_file_path} not found. call list_files_and_folders to list the files and folders in the current working directory "}
    

def terminate(message: str) -> str:
    """Terminate the conversation."""
    return  message