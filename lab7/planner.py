import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

URL = "https://router.huggingface.co/v1/chat/completions"


class Planner:
    def __init__(self, model = "Qwen/Qwen3.8-27B"):
        self.model = model
        self.token = os.getenv("HF_TOKEN2")

    def create_plan(self, goal) -> dict:

        HEADERS = {
            "Authorization":f"Bearer {self.token}",
            "Content-Type":"application/json"
        }

        prompt = f"""
You are task planner.

Break the users goal into small number of clear, executable tasks.

user goal is : {goal}

Return ONLY valid json in the given format as a dict in python:
{{
    "tasks":[
    {{
        "id":1,
        "description":"...",
        "status": "pending/in-progress/failed"
    }}
    ]
}}
Rules:
- Tasks must be concrete.
- Tasks must contribute to the goal.
- Avoid unnecessary tasks.
- order tasks logically.
"""
        payload = {
            "model":self.model,
            "messages":[{"role":"user", "content":prompt}],
            "max_tokens":2500,
        }
        response = requests.post(
            url=URL,
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        content =  data['choices'][0]['message']['content'] #['choices'][0]['message']['content']
        plan = json.loads(content)
        return plan

# plan = Planner()
# res = plan.create_plan("Compare  FastAPI and Django as backend framework and then gimme a verdict")
# print(type(res))      
# print(res)      
