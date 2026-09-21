from agent import run_agent


print("---Niggagent activated---")
while True:
    user_ip = input("\n>> ")

    if user_ip.lower() in {'exit','quit','gtfo'}:
        break

    try:
        ans = run_agent(user_ip)
        print('\nniggagent>>',ans)
    except Exception as e:
        print(f'\nniggagent>> {e}')
        
