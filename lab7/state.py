from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    """this is the runtime state of the agent"""
    goal : str 
    plan : list[Any] = field(default_factory=list)
    current_task : Any | None = None
    completed_task : list[Any] = field(default_factory=list)
    results : list[Any] = field(default_factory=list)
    iteration : int = 0
