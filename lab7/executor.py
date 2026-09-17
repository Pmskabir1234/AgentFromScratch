import requests
from tools import tools_schemas
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://router.huggingface.co/v1/chat/completions"

class Executor:
    def __init__(self, model = "Qwen/Qwen3.8-27B"):
        self.model = model
        self.token = os.getenv("HF_TOKEN2")

    def execute(self, task : dict, previous_results):
        HEADERS =  {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"

        }

        prompt = f"""
You are an execution agent.

Current task:
{task['description']}

Previous Findings: 
{previous_results}

now, your job is complete the current task.

Return a concise and to the point result containing:
1.What u discovered
2.Evidence/reasoning
3.Limitations(if any)"""
        message = [{
                "role":"user",
                "content":prompt
            }]
        payload = {
                "model":self.model,
                "messages":message,
                "tools":tools_schemas,
                "tool_choice":"auto",
                "max_tokens":3000
            }
        response = requests.post(
                url=URL,
                headers=HEADERS,
                json=payload
            )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

# task = {
#     "description":'compare FastAPI and Django'
# }
# prev = []     
# exe = Executor()
# res = exe.execute(task=task, previous_results= prev)
# print(res)
