from rich.console import Console
from rich.table import Table

from src.utils.logger import DualLogger
from src.globals import *

logger = DualLogger("Formatters", "formatters.log", console=CONSOLE_LOGGING, debug=ENABLE_DEBUG_LOGGING)

console = Console()

class UserFormatters:
    def user_table(*users):
        if not users:
            raise RuntimeError("No users were provided to UserFormatter.")
        
        
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("Projects")
        
        # for user in users:
            # projects_str = "\n".join([project.title for project in user.projects])
            # table.add_row(user.name, user.email, projects_str)
        
        console.print(table)
    



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
