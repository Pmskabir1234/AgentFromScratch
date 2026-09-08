# objective: understanding agent loop 

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv("HF_TOKEN")
MODEL = "Qwen/Qwen3.8-27B"

URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def calculator(expression: str) -> str:
    """calcualate mathematical exresssions"""
    return str(eval(expression))


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression such as 12 * 5"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


messages = [
    {
        "role": "user",
        "content": "what is answer of 1.2*9.11/4.1"
    }
]


def call_llm(messages : list):
    payload = {
        "model":MODEL,
        "messages":messages,
        "tools":tools,
        "tool_choice":'auto',
        "max_tokens":1000
    }

    response = requests.post(
        url=URL,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]

# now comes the agent loop 
while True:
    print("---Calling LLM---")

    msg = call_llm(messages)
    print(f"\nLLM message: {msg}")

    # if tools got called
    tool_calls = msg.get("tool_calls") 

    if not tool_calls:
        print(f"\nFinal Answer: {msg.get('content')}")
        break

    print("--TOOL CALL DETECTED---")
    messages.append(msg)

    for tool_call in tool_calls:
        tool_call_id = tool_call['id']
        function_name = tool_call['function']['name']

        arguments = json.loads(
            tool_call['function']['arguments']
        )

        print("\nFunction: ",function_name)
        print("Arguments: ",arguments)

        if function_name == 'calculator':
            result = calculator(
                arguments['expression']
            )
        else:
            result = f"Unknown tool: {function_name}"

        print("Tool result: ",result)

        # sending back tool result into conversation
        messages.append({
            "role":'tool',
            "tool_call_id":tool_call_id,
            "content":result
        })
    print("\nSending tool result back to LLM...")