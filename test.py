import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HF_TOKEN")

print("Token loaded:", bool(token))
print("Token prefix:", token[:7] if token else None)

# URL = "https://router.huggingface.co/v1/chat/completions"
# MODEL = "Qwen/Qwen3.8-27B"

# headers = {
#     "Authorization": f"Bearer {token}",
# }
# messages = [
#     {
#         "role":"user",
#         "content":"what is todays temperature in kolkata?"
#     }
# ]
# payload = {
#     "model":MODEL,
#     "messages":messages,
#     "max_tokens":1500
# }
# response = requests.post(
#     url=URL,
#     headers=headers,
#     json=payload
# )

# raw = response.json()
# print(raw.keys(), '\n')
# print(raw['choices'][0]['message']['content'])

city = "Malda"
population_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

response = requests.get(
    url=population_url
)


data = response.json()

a = data['results'][0]['population']
print(a)