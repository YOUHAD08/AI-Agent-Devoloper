
from action_registry import ActionRegistry
from action import Action
from tools import *


file_management_registry = ActionRegistry()
file_management_registry.register_action(
    Action(
      name="list_files", 
      function=list_files,
      description="List all files in the current directory",
      parameters={
          "type": "object",
          "properties": {},
          "required": [],
      },
))
file_management_registry.register_action(
    Action(
      name="read_file",
      function=read_file,
      description="Read the contents of the specified file",
      parameters={
          "type": "object",
          "properties": {
              "file_path": {
                  "type": "string",
                  "description": "The path to the file to read"
              }
          },
          "required": ["file_path"],
      }
))

file_management_registry.register_action(
  Action(
      name="search_in_file",
      function=search_in_file,
      description="Search for a term in the specified file",
      parameters={
          "type": "object",
          "properties": {
              "file_path": {
                  "type": "string",
                  "description": "The path to the file to search"
              },
              "search_term": {
                  "type": "string",
                  "description": "The term to search for in the file"
              }
          },
          "required": ["file_path", "search_term"],
      }
  ))