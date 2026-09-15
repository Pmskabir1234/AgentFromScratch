import requests
from memory import save_memory,load_memory,forget,remember,retrieve


ARTICLES = {
    "python gil": [
        "The Global Interpreter Lock historically prevents multiple Python threads from executing Python bytecode simultaneously in CPython.",
        "The GIL has implications for CPU-bound multithreaded programs.",
        "Multiprocessing can provide parallelism by using separate processes."
    ]
}

def calculator(expression: str) -> str:
    """calcualate mathematical exresssions"""
    try:
        return str(eval(expression))
    except:
        return "Calculator Error!"

    
def get_population(city: str) -> str:
    """get the population data for the given city"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(
        url
    )
    data = response.json()
    return f"{data['results'][0]['population']}"

def search(query:str) -> str:
    "search article for the given query"
    query = query.lower()
    res = ARTICLES.get(
        query,
        ['result not found :(']
    )
    return "\n".join(res)


tools_schemas = [
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
    },
    {
        "type":"function",
        "function":{
            "name":"get_population",
            "description":"get population data for a city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"Get the population of the given city"
                    }
            },
            "required":["city"]
        }
    }
    },
    {
        "type":"function",
        "function":{
            "name":"search",
            "description":"search for articles asked in query",
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"the article asked by user"
                    }
                },
               "required":['query'] 
            }
        }
    }
    
]

TOOLS = {
    "calculator":calculator,
    "get_population":get_population,
    "search":search,
}