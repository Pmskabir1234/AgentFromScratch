from planner import Planner
from state import AgentState
from executor import Executor
from rich.console import Console
from rich.rule import Rule
from rich.table import Table
from rich.live import Live


console = Console()

def run_agent(goal):

    state = AgentState(goal=goal)
    planner = Planner()
    ex = Executor()

    state.goal = goal

    # here we'll create a plan
    plan_result = planner.create_plan(goal)
    state.plan = plan_result['tasks']

    def build_plan_table(state):
        table = Table(
            title="Execution Plan",
            header_style="bold yellow"
        )

        table.add_column("ID", justify="center")
        table.add_column("Task")
        table.add_column("Status")

        # for mapping task states dynamically
        STATUS_DISPLAY = {
            "pending":"[yellow]Pending[/]",
            "in_progress":"[cyan]Running[/]",
            "completed":"[green]Done[/]",
            "failed":"[red]Failed[/]"
        }
        for task in state.plan:
            table.add_row(
                str(task['id']),
                task['description'],
                STATUS_DISPLAY.get(task['status'], task['status'])
            )

        return table

    console.print(Rule("[bold cyan]Execution starting[/]"))
    with Live(build_plan_table(state), console=console, refresh_per_second=1) as live:
        for task in state.plan:
            task['status'] = "in_progress"
            state.current_task = task

            live.update(build_plan_table(state))

            # print("Executing: ",task['description'],'\n')

            with console.status(f"[bold cyan] Executing : {task['description']}[/]"):
                res = ex.execute(task,state.results)

            state.results.append(res)
            

            state.completed_task.append(task)
            task['status'] = "completed"
            live.update(build_plan_table(state))
    return state.results[-1]
    # print(state.results)

# run_agent("compare FastAPI and Django as backend framewroks and gimme a verdict")