from planner import Planner
from state import AgentState
from executor import Executor

def run_agent(goal):

    state = AgentState(goal=goal)
    planner = Planner()
    ex = Executor()

    state.goal = goal

    # here we'll create a plan
    plan_result = planner.create_plan(goal)
    state.plan = plan_result['tasks']

    print("\nPlan: ")
    for task in state.plan:
        print(
            f"Task id: {task['id']}\t Description: {task['description']} \n",
        )

    print("-"*100, "\nExecution starting...\n")
    for task in state.plan:
        task['status'] = "in_progress"
        state.current_task = task

        print("Executing: ",task['description'],'\n')

        res = ex.execute(task,state.results)

        state.results.append(res)
        

        state.completed_task.append(task)
        task['status'] = "completed"
    return state.results[-1]
    # print(state.results)

# run_agent("compare FastAPI and Django as backend framewroks and gimme a verdict")