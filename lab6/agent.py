import os
from dotenv import load_dotenv
import requests
import json
from lab6.tools import tools, TOOLS
load_dotenv()



class Agent:
    def __init__(self, model:str):
        self.model = model
        self.token = os.getenv('HF_TOKEN')


    def _execute_tool(self, name, arguments: dict):

        tool_ = TOOLS.get(name, None)
        if tool_ is None:
            raise ValueError(f"Unknow tool: {name}")
        return tool_(**arguments)
        

    def _llm_response(self,message: list):
        URL = "https://router.huggingface.co/v1/chat/completions"
        HEADERS = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json",
        }
        payload = {
            "model":self.model,
            "messages":message,
            "max_new_tokens":1000,
            "tools":tools,
            "tool_choice":"auto"
        }
        result = requests.post(
            url=URL,
            headers=HEADERS,
            json=payload
        )
        data = result.json()
        return data['choices'][0]['messages']




    def run(self, user_input: str):
        m = [{
            "role":"user",
            "content":user_input
        }]

        llm_result = self._llm_response(m)



        


