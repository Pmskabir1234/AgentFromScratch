# AgentFromScratch

A hands-on, lab-by-lab walkthrough of how to build an LLM agent from the ground up in plain Python, without relying on a heavyweight agent framework. Each lab adds one new concept on top of the previous one, starting from a simple chat loop and ending with a reusable agent class that supports tool calling and multi-step reasoning.

## Purpose

This repository is a learning project. Instead of jumping straight to a framework like LangChain's agent abstractions, it rebuilds the core pieces of an agent step by step:

1. Sending a message to an LLM and printing the response.
2. Giving the LLM a tool and manually running the "agent loop" (call model, detect tool call, run tool, send result back).
3. Turning ad hoc tool handling into a proper tool registry and generic executor.
4. Wrapping all of this into a reusable `Agent` class with iteration limits and conversation memory.

## Models Used

All labs call hosted models through the Hugging Face Inference API (`HF_TOKEN` environment variable), either via LangChain's `ChatHuggingFace` wrapper or via direct HTTP requests to the Hugging Face router endpoint.

| Lab | Interface | Model |
|---|---|---|
| `lab1.py` | `langchain_huggingface.ChatHuggingFace` + `HuggingFaceEndpoint` | `google/gemma-4-31B-it` |
| `lab2.py`, `lab3.py` | Raw REST calls to `https://router.huggingface.co/v1/chat/completions` | `Qwen/Qwen3.8-27B` |
| `lab4-5/agent.py` | Raw REST calls to the same router endpoint, wrapped in an `Agent` class | `Qwen/Qwen3.8-27B` (default, configurable via the `Agent(model=...)` argument) |
| `lab6/agent.py` | Raw REST calls to the same router endpoint | Configurable via the `Agent(model=...)` argument |

The router endpoint follows the OpenAI-style `chat/completions` schema (`messages`, `tools`, `tool_choice`, `tool_calls`), which is why the request/response handling looks similar across labs even though the underlying model changes.

## Repository Structure

```
AgentFromScratch/
├── lab1.py            # Terminal -> Python -> LLM API -> response -> terminal
├── lab2.py            # First agent loop: LLM + one tool (calculator)
├── lab3.py            # Tool registry and generic tool executor
├── lab4-5/
│   ├── agent.py       # Agent class: state, iteration limit, conversation memory
│   ├── tools.py       # Tool implementations and JSON schemas
│   └── main.py        # Interactive CLI that drives the Agent class
├── lab6/
│   ├── agent.py        # Further iteration on the Agent class
│   └── tools.py        # Tool implementations and JSON schemas
├── test.py             # Scratch file for checking the HF token and API calls
└── requirements.txt    # Python dependencies
```

## Lab-by-Lab Breakdown

### `lab1.py` — Basic LLM Call
Objective: `terminal -> python -> LLM API -> response -> terminal`.
Uses `ChatHuggingFace` with a `HuggingFaceEndpoint` pointed at `google/gemma-4-31B-it` to build a minimal REPL (`terminal_buddy`) that sends whatever the user types and prints the model's reply, looping until the user types `exit`.

### `lab2.py` — Understanding the Agent Loop
Objective: understand the core agent loop.
Defines a single tool, `calculator`, and its JSON schema, then implements the loop manually:
1. Send the conversation to the model with `tools` and `tool_choice="auto"`.
2. If the model returns `tool_calls`, execute the requested tool and append a `role: "tool"` message with the result.
3. Repeat until the model responds with plain content instead of a tool call.

### `lab3.py` — Tool Registry and Generic Executor
Objective: introduce the concept of a tool registry.
Adds a second tool, `get_population` (queries the Open-Meteo geocoding API), and replaces the `if/elif` tool dispatch from `lab2.py` with a `TOOLS` dictionary and a generic `execute_tool(name, arguments)` function that looks up and calls the right tool by name.

### `lab4-5/` — Agent Class, Iteration Limit, and Memory
Objective: turn iteration count into a stop condition and add conversation memory.
- `tools.py` holds the tool implementations (`calculator`, `get_population`) and their schemas, imported by the agent.
- `agent.py` defines:
  - `AgentState`, a small container for messages, tool results, iteration count, and goal.
  - `Agent`, a class that wraps the model name, a `max_iter` cap (default 10), the Hugging Face token, and an `AgentState` instance. Its `run(user_input)` method repeats the call-model / detect-tool-call / execute-tool / append-result cycle up to `max_iter` times, returning the final text answer once the model stops calling tools, or reporting that the iteration limit was reached.
- `main.py` is a simple CLI loop that instantiates `Agent()` and calls `agent.run(user_input)` for each line of input, exiting on `exit`, `quit`, or a custom quit keyword.

### `lab6/` — Further Iteration on the Agent Class
Continues refactoring the same `Agent` pattern (constructor takes an explicit `model` argument, tools imported from `lab6/tools.py`). This lab is in progress: `run()` currently only sends the first user message to the model and does not yet loop on tool calls the way `lab4-5/agent.py` does.

### `test.py`
A scratch script used to confirm that `HF_TOKEN` is being loaded correctly from the environment and to try out raw calls to the Hugging Face router and the Open-Meteo geocoding API independently of the agent code.

## Tools Implemented

- **`calculator(expression: str)`** — evaluates a mathematical expression string with Python's `eval` and returns the result as a string.
- **`get_population(city: str)`** — looks up a city through the Open-Meteo geocoding API (`https://geocoding-api.open-meteo.com/v1/search`) and returns its population.

Both tools are exposed to the model as OpenAI-style function-calling schemas (`type: "function"`, with a `name`, `description`, and JSON Schema `parameters`).

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with your Hugging Face token:
   ```
   HF_TOKEN=your_huggingface_token_here
   ```
3. Run any lab directly, for example:
   ```
   python lab1.py
   python lab2.py
   python lab3.py
   python lab4-5/main.py
   ```

## Dependencies

Listed in `requirements.txt`:
- `langchain`
- `langchain-huggingface`
- `huggingface-hub`
- `python-dotenv`

`lab2.py`, `lab3.py`, `lab4-5/`, and `lab6/` also use the standard `requests` and `json` libraries for direct HTTP calls to the Hugging Face router endpoint.

## Notes and Known Limitations

- The `calculator` tool uses `eval` on the raw expression string, which is fine for a learning exercise but is not safe for untrusted input in a production system.
- `lab6/agent.py` is a work in progress: it imports `tools` from `lab6/tools.py` (the module actually defines `tools_schemas`), and its `_llm_response` method reads `data['choices'][0]['messages']` instead of `data['choices'][0]['message']`. The `run` method does not yet loop on tool calls.
- Some print statements and identifiers in `lab4-5/agent.py` and `lab4-5/main.py` use casual, informal language left over from development and are worth cleaning up before sharing the code more broadly.
- Model names such as `google/gemma-4-31B-it` and `Qwen/Qwen3.8-27B` are passed as-is to the Hugging Face router; verify current availability and exact naming on Hugging Face before relying on them.
