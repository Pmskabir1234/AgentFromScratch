import json
from pathlib import Path
from typing import Any

MEMORY_FILE = Path("memory.json")

def load_memory() -> dict[str, Any]:
    """load persistent memory from disk"""

    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE,"r",encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError,OSError):
        return {"message":"error related to json decoder"}

def save_memory(memory: dict[str, Any]) -> None:
    """save persistent memory to disk"""

    with open(MEMORY_FILE, 'w', encoding="utf-8") as f:
        json.dump(
            memory, f, indent=4,ensure_ascii=False
        )

def remember(key: str, value: Any)  -> None:
    """store or update a memory"""

    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def retrieve(key:str, default: Any=None) -> Any:
    """retrieve a memory by key"""
    memory = load_memory()
    return(memory.get(key, default))

def forget(key:str) -> None:
    """remove a specific memory by key"""
    memory = load_memory()
    if key in memory:
        del memory[key]
    save_memory()