from langchain_core.language_models import BaseChatModel
from langgraph.constants import END
from langgraph.graph import StateGraph

from agents import PlannerAgent, ArchitectAgent, CoderAgent


class CantataAgent:
    def __init__(self, llm: BaseChatModel, recursion_limit: int = 100) -> None:
        self._recursion_limit = recursion_limit

        planner = PlannerAgent(llm)
        architect = ArchitectAgent(llm)
        coder = CoderAgent(llm)

        self._graph = self._build(planner, architect, coder)

    def run(self, user_prompt: str) -> dict:
        return self._graph.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": self._recursion_limit},
        )

    @staticmethod
    def _build(
        planner: PlannerAgent,
        architect: ArchitectAgent,
        coder: CoderAgent,
    ) -> object:
        graph = StateGraph(dict)

        graph.add_node("planner", planner.run)
        graph.add_node("architect", architect.run)
        graph.add_node("coder", coder.run)

        graph.add_edge("planner", "architect")
        graph.add_edge("architect", "coder")

        graph.add_conditional_edges(
            "coder",
            lambda state: "END" if state.get("status") == "DONE" else "coder",
            {"END": END, "coder": "coder"},
        )

        graph.set_entry_point("planner")
        return graph.compile()
