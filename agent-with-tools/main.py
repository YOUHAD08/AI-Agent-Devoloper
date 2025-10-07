from litellm import completion
import json
from config import agent_rules , tool_functions, tools


print("AI: Hello! I am your AI assistant. How can I help you today?")
messages = agent_rules 
while True:
  user_input = input("User : ")
  if user_input.lower() in ["exit", "quit", "stop"]:
      print("AI: Goodbye!")
      break
  
  messages.append({"role": "user", "content": user_input})

  print("AI:  Executing the task...")
  while True:
    response = completion(
            model="openai/gpt-4o",
            messages=messages,
            tools=tools,
            max_tokens=1024
        )
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls :
        tool_name = tool_calls[0].function.name
        tool_args = json.loads(tool_calls[0].function.arguments)
        action = {
            "tool_name": tool_name,
            "args": tool_args
        }
        result = tool_functions[tool_name](**tool_args)
        if tool_name == "terminate":
            print(f"AI: {result}")
            break


        messages.extend([
                    {"role": "assistant", "content": json.dumps(action)},
                    {"role": "user", "content": json.dumps(result)}
                ])
    else:
        assistant_message = response.choices[0].message.content
        print(f"AI: {assistant_message}")
        break   