from dotenv import load_dotenv
import os
from litellm import completion
from typing import List, Dict
import re


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="gpt-4o",  # you don’t need "openai/" prefix
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

def extract_code_blocks(response: str) -> str:
    """Extract code blocks from the text"""
    code_blocks = response.strip().split("```")[1][6:].strip()
    return code_blocks if code_blocks else response

def extract_function_name_from_code(code: str) -> str:
    """Extract function name from code"""
    match = re.search(r'def (\w+)\s*\(', code)
    return match.group(1) if match else "unknown_function"

messages = [
    {
        "role": "system",
        "content": 
            "You are an expert software engineer specializing in functional programming with Python. "
            "Your task is to provide only code, without explanations or commentary, unless explicitly requested. "
            "All code generated in this conversation must be contained within a single code block."
    }
]


while True:
    user_input = input("User: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    messages.append({"role": "user", "content": user_input})
    response = generate_response(messages)
    print(f"AI: {response}")
    response = extract_code_blocks(response)
    print(f"Extracted Code:\n{response}")
    messages.append({"role": "assistant", "content": response})

print("Saving to file...")
print(messages[-1]["content"])

with open(rf"./code-generated/{extract_function_name_from_code(messages[-1]['content'])}.py", "w") as file:
    file.write(messages[-1]["content"])

print("File saved successfully!")