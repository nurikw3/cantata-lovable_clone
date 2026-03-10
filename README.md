# Cantata — Lovable Clone

> An AI-powered code generation agent that turns a plain text prompt into a fully working project — files, structure, and all.

---

## How it works

Cantata uses a multi-agent pipeline built on **LangGraph** to go from a user prompt to a ready-to-run project in three stages:

```
User Prompt → [Planner] → [Architect] → [Coder × N] → generated_project/
```

| Agent | Role |
|---|---|
| **Planner** | Understands the request and produces a high-level plan |
| **Architect** | Breaks the plan into concrete implementation steps with file paths |
| **Coder** | Executes each step one by one — reads, writes, and runs shell commands |

Each Coder step is a **ReAct loop** with access to filesystem and shell tools.

---

## Tech stack

- **Python** — core language
- **LangGraph** — stateful multi-agent orchestration
- **LangChain** — LLM tooling and structured output
- **Groq API** — model inference (`openai/gpt-oss-120b`)
- **pydantic-settings** — configuration via `.env`
- **Rich** — terminal UI

---

## Coder tools

| Tool | What it does |
|---|---|
| `write_file` | Writes content to a file inside `generated_project/` |
| `read_file` | Reads an existing file |
| `list_files` | Lists all files in a directory |
| `get_current_directory` | Returns the project root path |
| `run_cmd` | Executes shell commands (e.g. `npm install`, `ls`) |

All file operations are sandboxed — the agent cannot write outside `generated_project/`.

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/nurikw3/cantata-lovable_clone
cd cantata-lovable_clone
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run

```bash
uv run main.py
```

Enter a prompt when asked and the generated project will appear in `./generated_project/`.

---

## Example prompts

```
Build a colourful modern todo app in HTML, CSS and JS
Create a REST API in Python with FastAPI that manages a book library
Build a markdown blog with Next.js and Tailwind CSS
```

---

## Project structure

```
cantata-lovable_clone/
├── main.py               # Entry point and CLI prompt
├── graph.py              # CantataAgent — assembles and runs the LangGraph pipeline
├── agents.py             # PlannerAgent, ArchitectAgent, CoderAgent
├── config.py             # Settings via pydantic-settings
├── states.py             # Pydantic models: Plan, TaskPlan, CoderState
├── prompts.py            # System and user prompts for each agent
├── tools.py              # Filesystem and shell tools
├── tui.py                # Rich terminal UI
├── .env                  # API keys (not committed)
└── generated_project/    # Output — everything the agent generates goes here
```

---

## Notes

- `recursion_limit` is set to 100 to support projects with many files
- Each Coder step is isolated — if one step fails, the loop continues to the next
- The Coder always writes complete file contents, not diffs or snippets

---

## License

MIT
