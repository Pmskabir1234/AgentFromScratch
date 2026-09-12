import os
from dotenv import load_dotenv
import requests
import json
from tools import tools_schemas, TOOLS
from state import AgentState
load_dotenv()




class Agent:
    def __init__(self, model: str = "Qwen/Qwen3.8-27B"):
        self.model = model
        self.state = AgentState()
        self.max_iterations = 5
        self.token = os.getenv('HF_TOKEN')

    def _execute_tool(self, name, arguments: dict):

        tool_ = TOOLS.get(name, None)
        if tool_ is None:
            raise ValueError(f"Unknow tool: {name}")
        
        try:
            return tool_(**arguments)
        except Exception as e:
            return f"Seems like something gone wrong : {e}"
        

    def _llm_response(self,message: list):
        URL = "https://router.huggingface.co/v1/chat/completions"
        HEADERS = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json",
        }
        payload = {
            "model":self.model,
            "messages":message,
            "max_tokens":1000,
            "tools":tools_schemas,
            "tool_choice":"auto"
        }
        result = requests.post(
            url=URL,
            headers=HEADERS,
            json=payload
        )
        result.raise_for_status()
        data = result.json()
        return data['choices'][0]['message']




    def run(self, user_input: str):
        self.state.add_user_message(user_input)
        
        for _ in range(self.max_iterations):
            self.state.iteration_incerement()
            print("---Calling LLM---\n")
            llm_result = self._llm_response(self.state.messages)
            print(f"LLM Message: {llm_result}")
            self.state.add_assistant_message(llm_result)
            called_tools =  llm_result.get('tool_calls')  
            if not called_tools:
               return f"\nFinal answer: {llm_result.get('content')}"

            print("\nTool call detetcted!")

            for tool in called_tools:
                tool_call_id = tool['id']
                func_name = tool['function']['name']
                args = json.loads(
                    tool['function']['arguments']
                )

                print(f"\nFuntion name: {func_name}")
                print(f"Argument: {args}")

                tool_result = self._execute_tool(name=func_name,arguments=args)
                print(f"Tool result: {tool_result}")
                self.state.add_tool_result(tool_call_id, func_name, tool_result)

            print("sending tool result back to llm!\n")
        return f"oops, before we get you final answer maximum iters reached!"




        


