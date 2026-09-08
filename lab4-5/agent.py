from tools import TOOLS, tools_schemas
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()



class AgentState:
    def __init__(self):
        self.messages = []
        self.tool_results = []
        self.iteration = 0
        self.goal = None


class Agent:
    def __init__(self, model : str = "Qwen/Qwen3.8-27B"):
        self.model = model
        self.max_iter = 10
        self.token = os.getenv('HF_TOKEN')
        self.history = AgentState()

    
    def _execute_tool(self, name, arguments):
        tool = TOOLS.get(name)

        if tool is None:
            return "Unknown tool: {name}"

        try:
            return tool(**arguments)
        except Exception as e:
            return f"Tool (bekar) error: {e}"

    def _llm_response(self, messages : list):
        URL = "https://router.huggingface.co/v1/chat/completions"
        HEADERS = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type":"application/json"
        }
        payload = {
            "model":self.model,
            "messages":messages,
            "tools":tools_schemas,
            "tool_choice":"auto",
            "max_tokens":1000
        }
        response = requests.post(
            url=URL,
            headers=HEADERS,
            json=payload   
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]['message']

    def run(self, user_input):
        mg = self.history.messages
        query = {
                    "role":"user",
                    "content":user_input
                }
        mg.append(query)
        for i in range(self.max_iter):
            print("---Calling LLM---")

            llm_message = self._llm_response(messages=mg)
            mg.append(llm_message)
            print("\nLLM message: ", llm_message)

            tools_called = llm_message.get("tool_calls")
            if not tools_called:
                return f"\nFinal answer: {llm_message.get("content")}"

            print("\n---TOOL CALL DETECTED---")
            # mg.append(llm_message)

            for tool in tools_called:
                tool_id = tool['id']
                function_name = tool['function']['name']
                arguments = json.loads(
                    tool['function']['arguments']
                )

                print("\nFunction Name: ",function_name)
                print("\nArguments: ",arguments)

                result = self._execute_tool(function_name,arguments)

                print("\n---Tool Result---\n",result)

                mg.append({
                    "role":"tool",
                    "tool_call_id":tool_id,
                    "content":result
                })
                self.history.tool_results.append({
                    "role":"tool",
                    "tool_call_id":tool_id,
                    "content":result
                })
            print("\nSending result back to LLM...\n")
        print("Nigga agent stopped, maximum iterations reached!")


            

