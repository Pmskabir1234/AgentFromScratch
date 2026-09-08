# objective : terminal -> python -> LLM API -> response -> terminal

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    model='google/gemma-4-31B-it',
    task='text-generation',
    max_new_tokens=1000
)
model = ChatHuggingFace(llm=llm)

def terminal_buddy(model):
    messages = [
        {   
            'role':'user',
            'content' : []
        },
        {   
            'role':'ai',
            'content' : []
        }

    ]
    print("-------Hello! I am here to assist you...--------")
    while True:
        user_input = input("\n> ")

        if user_input.lower() == 'exit':
            break


        messages[0]['content'].append(user_input)
        response = model.invoke(messages[0]['content'])
        messages[1]['content'].append(response.content)
        print('\nneo: ', response.content)

terminal_buddy(model)




