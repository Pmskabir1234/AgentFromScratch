from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    """this is the runtime state of the agent"""
    # for current convo
    messages : list[dict[str,Any]] = field(default_factory=list)

    # tools results returned during current task
    tool_results : list[dict[str, Any]] = field(default_factory=list)

    # current objective
    goal : str | None = None

    iteration : int = 0

    final_answer : str | None = None

    finished : bool = False

    def add_user_message(self, content: str):
        """adding user message to the conversation"""
        self.messages.append({
            "role":"user",
            "content":content
        })

    def add_assistant_message(self, msg: dict | None = None, tool_calls: list[dict[str, Any]] | None = None):
        """add assistant message (including message containing tool calls)"""
        # msg : dict[str, Any] = {"role":"assistant"}

        if msg is not None:
            # msg['content'] = content
            self.messages.append(msg)
        # if tool_calls:
        #     msg['tool_calls'] = tool_calls
        # self.messages.append(msg)

    def add_tool_result(self,tool_call_id:str ,tool_name:str, result: str):
        """adding tool execution result following chat completion tool message format"""

        self.messages.append({
            "role":"tool",
            "tool_call_id":tool_call_id,
            "tool_name":tool_name,
            "content":str(result)
        })
        self.tool_results.append({
            "tool_call_id":tool_call_id,
            "tool_name":tool_name,
            "result":result
        })

    def iteration_incerement(self):
        self.iteration += 1

    def finish(self, answer: str):
        self.final_answer = answer
        self.finished = True
