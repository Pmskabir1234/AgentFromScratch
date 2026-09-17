import requests
import time


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
    }   
]

TOOLS = {
    "calculator":calculator,
    "get_population":get_population
}