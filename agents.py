from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel

from tools import write_file, read_file, list_files, run_cmd, get_current_directory
from states import Plan, TaskPlan, CoderState
from prompts import planner_prompt, architect_prompt, coder_system_prompt
from tui import (
    print_phase,
    print_step_table,
    print_step_header,
    print_step_done,
    print_step_error,
    spinner,
)


class PlannerAgent:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm

    def run(self, state: dict) -> dict:
        with spinner("Planner — analysing prompt ...") as p:
            p.add_task("")
            resp = self._llm.with_structured_output(Plan).invoke(
                planner_prompt(state["user_prompt"])
            )
        print_phase("planner", "plan produced")
        return {"plan": resp}


class ArchitectAgent:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm

    def run(self, state: dict) -> dict:
        with spinner("Architect — scheduling steps ...") as p:
            p.add_task("")
            resp = self._llm.with_structured_output(TaskPlan).invoke(
                architect_prompt(state["plan"])
            )
        if resp is None:
            raise ValueError("Architect agent failed to produce a task plan.")

        n = len(resp.implementation_steps)
        print_phase("architect", f"{n} step{'s' if n != 1 else ''} scheduled")
        print_step_table(resp.implementation_steps)
        return {"task_plan": resp}


class CoderAgent:
    _TOOLS = [read_file, write_file, list_files, get_current_directory, run_cmd]

    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm
        self._react = create_react_agent(llm, self._TOOLS)

    def run(self, state: dict) -> dict:
        coder_state: CoderState = state.get("coder_state")

        if coder_state is None:
            coder_state = CoderState(
                task_plan=state["task_plan"],
                current_step_idx=0,
            )

        steps = coder_state.task_plan.implementation_steps

        if coder_state.current_step_idx >= len(steps):
            return {"coder_state": coder_state, "status": "DONE"}

        idx = coder_state.current_step_idx
        task = steps[idx]
        total = len(steps)

        print_step_header(idx + 1, total, task.filepath, task.task_description)

        existing_content = self._read_existing(task.filepath)
        existing_info = (
            f"\nExisting content:\n{existing_content}\n"
            if existing_content
            else "\nThis is a new file.\n"
        )

        user_prompt = (
            f"Task: {task.task_description}\n"
            f"File: {task.filepath}\n"
            f"{existing_info}\n"
            f"CRITICAL REMINDERS:\n"
            f'- Use write_file(path="{task.filepath}", content="...") to save the file\n'
            f'- Commands must be STRINGS: run_cmd(cmd="ls -la") NOT run_cmd(cmd=["ls", "-la"])\n'
            f"- Write COMPLETE file content, not just snippets\n"
            f"- Make the code production-ready and fully functional\n\n"
            f"Complete this task now."
        )

        with spinner(f"Writing {task.filepath} ...") as p:
            p.add_task("")
            try:
                self._react.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": f"{coder_system_prompt()}\n\n{user_prompt}",
                            }
                        ]
                    }
                )
                print_step_done(task.filepath)
            except Exception as e:
                print_step_error(task.filepath, str(e))

        coder_state.current_step_idx += 1
        return {"coder_state": coder_state}

    @staticmethod
    def _read_existing(filepath: str) -> str:
        try:
            result = read_file.invoke({"path": filepath})
            return "" if result.startswith("⚠️") else result
        except Exception:
            return ""
