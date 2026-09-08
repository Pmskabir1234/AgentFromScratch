# Objective : iteration as stop cause and conversation memory 

from agent import Agent

agent = Agent()


print("----Niggagent----\n")
while True:
    user_input = input(">> ")

    if user_input.lower() in {"exit", "quit", "gtfo"}:
        break

    answer = agent.run(user_input=user_input)
    print("\nniggagent>> ", answer)