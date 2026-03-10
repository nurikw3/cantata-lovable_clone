from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

HEADER = """\
   ██████╗ █████╗ ███╗  ██╗████████╗ █████╗ ████████╗ █████╗
  ██╔════╝██╔══██╗████╗ ██║╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗
  ██║     ███████║██╔██╗██║   ██║   ███████║   ██║   ███████║
  ██║     ██╔══██║██║╚████║   ██║   ██╔══██║   ██║   ██╔══██║
  ╚██████╗██║  ██║██║ ╚███║   ██║   ██║  ██║   ██║   ██║  ██║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝"""

_PHASE_LABELS = {
    "planner": "PLANNER  ",
    "architect": "ARCHITECT",
    "coder": "CODER    ",
}


def print_header() -> None:
    console.print(Text(HEADER, style="bold cyan", justify="center"))
    console.print(
        Align.center(Text("AI-powered code generation agent", style="dim white"))
    )
    console.print()
    console.print(Rule(style="bright_black"))
    console.print()


def prompt_user() -> str:
    user_input = Prompt.ask("  [bold white]prompt[/bold white]", console=console)
    console.print()
    return user_input


def print_generating(user_prompt: str) -> None:
    console.print(
        f"  [bright_black]generating[/bright_black]  [white]{user_prompt}[/white]"
    )
    console.print()


def print_phase(name: str, detail: str = "") -> None:
    label = _PHASE_LABELS.get(name.lower(), name.upper().ljust(9))
    console.print(f"  [cyan]{label}[/cyan]  {detail}")


def print_step_table(steps: list) -> None:
    table = Table(
        box=box.SIMPLE_HEAD,
        border_style="bright_black",
        header_style="bold white",
        show_lines=False,
        pad_edge=False,
    )
    table.add_column("#", style="bright_black", width=4)
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Task", style="white")

    for i, step in enumerate(steps, 1):
        table.add_row(str(i), step.filepath, step.task_description)

    console.print()
    console.print(
        Panel(
            table,
            title="[bold white]Steps[/bold white]",
            border_style="bright_black",
            padding=(0, 1),
        )
    )
    console.print()


def print_step_header(idx: int, total: int, filepath: str, task: str) -> None:
    console.print(
        Rule(f"[bold white]Step {idx}/{total}[/bold white]", style="bright_black")
    )
    console.print(f"  [bright_black]file[/bright_black]  [cyan]{filepath}[/cyan]")
    console.print(f"  [bright_black]task[/bright_black]  {task}")
    console.print()


def print_step_done(filepath: str) -> None:
    console.print(
        f"  [bold green]done[/bold green]  [bright_black]{filepath}[/bright_black]"
    )


def print_step_error(filepath: str, error: str) -> None:
    console.print(
        f"  [bold red]fail[/bold red]  [bright_black]{filepath}[/bright_black]"
    )
    console.print(f"         [dim]{error}[/dim]")


def print_summary(steps_done: int, output_dir: str) -> None:
    console.print()
    console.print(Rule(style="bright_black"))
    console.print()

    stats = Table.grid(padding=(0, 4))
    stats.add_column(style="bright_black")
    stats.add_column(style="bold white")
    stats.add_row("steps completed", str(steps_done))
    stats.add_row("output", output_dir)

    console.print(
        Panel(
            Align.center(stats),
            title="[bold green]Generation complete[/bold green]",
            border_style="green",
            padding=(1, 4),
        )
    )
    console.print()


def print_error(error: str) -> None:
    console.print()
    console.print(
        Panel(
            f"[red]{error}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red",
            padding=(0, 2),
        )
    )
    console.print()


def spinner(label: str) -> Progress:
    """Context manager — shows a transient spinner while a block runs."""
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[white]{label}[/white]"),
        console=console,
        transient=True,
    )
