from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box
from rich.layout import Layout
from rich.panel import Panel

from src.utils.logger import DualLogger
from src.globals import *

logger = DualLogger(
    "Formatters", "formatters.log", console=CONSOLE_LOGGING, debug=ENABLE_DEBUG_LOGGING
)

console = Console()


class UserFormatter:
    def user_table(*users):
        if not users:
            raise RuntimeError("No users were provided to UserFormatter.")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("Projects")

        for user in users:
            projects_str = "\n".join([project.title for project in user.projects])
            table.add_row(user.name, user.email, projects_str)

        console.print(table)


class ProjectFormatter:
    def project_table(*projects):
        if not projects:
            raise RuntimeError("No projects were passed to ProjectFormatter")
        
        for project in projects:
            layout = Layout()
            layout.split_column(
                Layout(name="header"),
                Align(project.description),
                Align(f"Project contains {len(project.tasks)} tasks."),
            )
            layout["header"].split_row(
                Layout(Align(project.title, align="left")),
                Layout(Align(f"Due: {project.due_date}", align="right"))
            )
            
            console.print(Panel(layout, width=80, padding=0))
        
        
        # for project in projects:
        #     table = Table(show_header=True, header_style="bold yellow")
        #     table.add_column()
        #     table.add_row(Align(project.title, align="left"), Align(project.due_date, align="right"))
            
        #     table.box = box.SIMPLE_HEAD
            
        #     description_subtable = Table(show_header=False, show_lines=False)
        #     description_subtable.add_row(project.description)
        #     table.add_row(description_subtable)
            
        #     table.add_row(f"Includes {len(project.tasks)} tasks.")
        #     console.print(table)
            
            


"""
TODO LIST:

- Users
    - indv user
    - table for listing all
    
- Projects
    - table for indv project
        - title left justified, due date right justified, one row
        - description block
        - tasks in sub table
    - table for listing all projects
        - user's name header
        - title left justified, due date right justified, one row
        - description block
        - small row mentioning # of tasks
        
- Tasks
    - invd task
        - title, status, assigned to, one row
    - table for listing tasks
        - proj title header
        - subtable of tasks (to be reused in indv proj table)
"""
