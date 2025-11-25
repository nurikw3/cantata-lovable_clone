import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.constants import END 
from langgraph.graph import StateGraph
from tools import write_file, read_file, list_files, run_cmd, get_current_directory, init_project_root
from states import Plan, TaskPlan, CoderState
from prompts import planner_prompt, architect_prompt, coder_system_prompt


init_project_root()

llm = ChatGroq(
    model="openai/gpt-oss-120b", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

coder_tools = [read_file, write_file, list_files, get_current_directory, run_cmd]


def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if resp is None:
        raise ValueError("Architect agent failed to produce a task plan.")
    resp.plan = plan  
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    coder_state: CoderState = state.get("coder_state")
    
    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"], 
            current_step_idx=0
        )
    
    steps = coder_state.task_plan.implementation_steps
    
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}
    
    current_task = steps[coder_state.current_step_idx]
    
    existing_content = ""
    try:
        result = read_file.invoke({"path": current_task.filepath})
        if not result.startswith("⚠️"):
            existing_content = result
    except Exception as e:
        print(f"⚠️ Could not read {current_task.filepath}: {e}")
    
    system_prompt = coder_system_prompt()
    
    existing_info = f"\nExisting content:\n{existing_content}\n" if existing_content else "\nThis is a new file.\n"
    
    user_prompt = f"""Task: {current_task.task_description}
        File: {current_task.filepath}
        {existing_info}
        CRITICAL REMINDERS:
        - Use write_file(path="{current_task.filepath}", content="...") to save the file
        - Commands must be STRINGS: run_cmd(cmd="ls -la") NOT run_cmd(cmd=["ls", "-la"])
        - Write COMPLETE file content, not just snippets
        - Make the code production-ready and fully functional

        Complete this task now.
    """
    
    print(f"\n{'='*60}")
    print(f"📝 Step {coder_state.current_step_idx + 1}/{len(steps)}")
    print(f"📄 File: {current_task.filepath}")
    print(f"📋 Task: {current_task.task_description}")
    print(f"{'='*60}\n")
    

    react_agent = create_react_agent(llm, coder_tools)
    
    try:
        result = react_agent.invoke({
            "messages": [
                {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
            ]
        })
        print(f"✅ Completed step {coder_state.current_step_idx + 1}")
    except Exception as e:
        print(f"❌ Error in step {coder_state.current_step_idx + 1}: {e}")
        import traceback
        traceback.print_exc()
    

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}



graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)


graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")


graph.add_conditional_edges(
    "coder",
    lambda state: "END" if state.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"},
)

graph.set_entry_point("planner")

agent = graph.compile()

if __name__ == "__main__":
    print("🚀 Starting Lovable Clone Agent...\n")
    
    user_prompt = "Build a colourful modern todo app in html css and js"
    
    try:
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": 100}
        )
        print("\n" + "="*60)
        print("✅ Project generation completed!")
        print("="*60)
        print("\nFinal State:")
        print(f"  Status: {result.get('status', 'UNKNOWN')}")
        if result.get('coder_state'):
            print(f"  Steps completed: {result['coder_state'].current_step_idx}")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()