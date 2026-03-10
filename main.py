import traceback

from langchain_openai import ChatOpenAI

from config import Config
from graph import CantataAgent
from tools import init_project_root
from tui import print_header, prompt_user, print_generating, print_summary, print_error


def main() -> None:
    cfg = Config()
    init_project_root()

    llm = ChatOpenAI(
        model=cfg.model,
        api_key=cfg.api_key.get_secret_value(),
        base_url=cfg.base_url,
        temperature=cfg.temperature,
    )

    print_header()
    user_prompt = prompt_user()
    print_generating(user_prompt)

    agent = CantataAgent(llm, recursion_limit=cfg.recursion_limit)

    try:
        result = agent.run(user_prompt)
        steps_done = (
            result["coder_state"].current_step_idx if result.get("coder_state") else 0
        )
        print_summary(steps_done, cfg.output_dir)
    except Exception as e:
        print_error(str(e))
        traceback.print_exc()


if __name__ == "__main__":
    main()
