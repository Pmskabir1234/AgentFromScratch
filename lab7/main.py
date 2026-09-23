from agent import run_agent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule

console = Console()

console.print(Rule("[brown]ask Niggagent anything"))
while True:
    user_ip = input("\n>> ")

    if user_ip.lower() in {'exit','quit','gtfo'}:
        break

    try:
        ans = run_agent(user_ip)
        console.print(
            Panel(
                Markdown(ans),
                title="Niggagent",
                border_style="cyan",
                padding=(1,2)
            )
        )
    except Exception as e:
        console.print(Markdown(f'\nniggagent>> {e}'))
        
