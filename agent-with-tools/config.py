from tools import *

agent_rules = [
  {
    "role": "system",
  "content": """

  You are an AI agent that can perform tasks by using the available tools.

  - If the user asks about files, documents, or content: first list the files before attempting to read them.
  - Once you have completed the task and reached a final answer, terminate the conversation by calling the "terminate" tool. 
  - Do not continue beyond termination; I will deliver the final result to the user.
  -if 
  """
   }
]


tool_functions = {
    "list_files_and_folders": list_files_and_folders,
    "read_file": read_file,
    "print_current_working_directory":print_current_working_directory,
    "folder_or_file":folder_or_file,
    "terminate": terminate
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files_and_folders",
            "description": "Returns a list of files and folders in the specified directory in a clear bullet-point format.",
            "parameters": {"type": "object", 
                           "properties": {"directory": {"type": "string"}}, 
                           "required": ["directory"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file .",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "print_current_working_directory",
            "description": "print the full path of the current working directory.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "folder_or_file",
            "description": "decides if the given path is a folder or file .",
            "parameters": {
                "type": "object",
                "properties": {"folder_or_file_path": {"type": "string"}},
                "required": ["folder_or_file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation and no longer actions is required and returns the final message to the user.",
            "parameters": {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"]
            }
        }
    }
]