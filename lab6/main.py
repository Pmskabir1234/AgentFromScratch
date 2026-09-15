from agent import Agent

nigga = Agent()

print("---Niggagent activated---")
while True:
    user_ip = input("\n>> ")

    if user_ip.lower() in {'exit','quit','gtfo'}:
        break

    ans = nigga.run(user_ip)
    print('\nniggagent>>',ans)