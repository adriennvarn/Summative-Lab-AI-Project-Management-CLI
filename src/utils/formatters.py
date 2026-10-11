from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.columns import Columns

from src.utils.logger import DualLogger
from src.globals import *

logger = DualLogger(
    "Formatters", "formatters.log", console=CONSOLE_LOGGING, debug=ENABLE_DEBUG_LOGGING
)

console = Console()


class Formatter:
    def user_table(*users):
        if not users:
            raise RuntimeError("No users were passed to user_table.")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("Projects")

        for user in users:
            projects_str = "\n".join([project.title for project in user.projects])
            table.add_row(user.name, user.email, projects_str)

        console.print(table)

    def project_table(*projects):
        if not projects:
            raise RuntimeError("No projects were passed to task_table")

        for project in projects:
            layout = Layout()
            table = Table(show_header=False, width=75, box=box.SIMPLE)
            table.add_row(
                Text(project.title, justify="left"),
                Text(f"Due: {project.due_date}", justify="right"),
            )
            layout.split_column(
                table,
                Panel(Text(project.description), box.SIMPLE),
                Panel(
                    Text(f"Project contains {len(project.tasks)} tasks."),
                    box.SIMPLE,
                ),
            )

            console.print(Panel(layout, width=80))
    
    def task_table(*tasks):
        if not tasks:
            raise RuntimeError("No tasks were passed to task_table")
        
        table = Table("Title", "Status", "Assigned To")
        for task in tasks:
            table.add_row(task.title, task.status, task.assigned_to.name, style="underline")

        console.print(table)
