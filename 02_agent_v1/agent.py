from dotenv import load_dotenv
import os
from litellm import completion
from typing import List, Dict
import re
import json
from litellm.exceptions import RateLimitError
import time

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response, retry if rate limited"""
    retries = 3
    for attempt in range(retries):
        try:
            response = completion(
                model="gpt-4o",
                messages=messages,
                max_tokens=700
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            print(f"Rate limit hit, retrying... ({attempt+1}/{retries})")
            time.sleep(2 ** attempt)  # exponential backoff
    raise Exception("Failed after retries due to rate limit")

def extract_action_blocks(response: str) -> str:
    """Extract action blocks from the text"""
    action_blocks = response.strip().split("```")[1][4:].strip()
    return action_blocks if action_blocks else response

def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_action_blocks(response)
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}


def list_files(directory: str) -> List[str]:
    """List files and folders in the specified directory."""
    return os.listdir(directory)

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"

agent_rules = [
  {
    "role": "system",
    "content": """
      You are an AI agent that can perform tasks by using available tools.

      Available tools:

      ```json
        {
          "list_files": {
              "description": "Lists all files and folders in the specified directory.",
              "parameters": {
                  "directory": {
                      "type": "string",
                      "description": "The directory to list files and folders from."
                  }
              }
          },
          "read_file": {
              "description": "Reads the content of a file.",
              "parameters": {
                  "file_name": {
                      "type": "string",
                      "description": "The name of the file to read."
                  }
              }
          },
          "terminate": {
              "description": "Ends the agent loop and provides a summary of the task.",
              "parameters": {
                  "message": {
                      "type": "string",
                      "description": "Summary message to return to the user."
                  }
              }
          }
        }
     ```

    If a user asks about files, documents, or content, first list the files before reading them.

    When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.

    Important!!! Every response MUST have an action.
    You must ALWAYS respond in this format:

    <Stop and think step by step. Parameters map to args. Insert a rich description of your step by step thoughts here.>

    ```action
      {
          "tool_name": "insert tool_name",
          "args": {...fill in any required arguments here...}
      }
    ```
   """
   }
]

while True:
    user_input = input("User: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    user = [{"role": "user", "content": user_input}]
    messages = agent_rules + user
    print("AI is thinking...")
    while True:
      response = generate_response(messages)
      action=parse_action(response)
      if action["tool_name"] == "terminate":
          print(f"AI: {action['args']['message']}")
          break
      elif action["tool_name"] == "list_files":
          directory = action["args"].get("directory", ".")
          result = {"result": list_files(directory)}
      elif action["tool_name"] == "read_file":
          file_name = action["args"].get("file_name", "")
          result = {"result": read_file(file_name)}
      elif action["tool_name"] == "error":
          result = {"error": action["args"]["message"]}
      else:
          result = {"error": f"Unknown tool: {action['tool_name']}"}
      memory = [
          {"role": "assistant", "content": response}, 
          {"role": "user", "content": json.dumps(result)}
        ]
      messages += memory