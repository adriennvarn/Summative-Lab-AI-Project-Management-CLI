#! /usr/bin/env python3

from rich import print
from src.models.user import User

ENABLE_DEBUG_LOGGING = True

"""
cmds:
    -n, --name
    -e, --email
    -u, --user
    -t, --title
    -d, --description
    -p, --project

    add-user --name --email
    update-user --user               brings up interactive, update name and/or email
    remove-user --name
    view-users
    
    add-project --user --title       brings up interactive inputs to add description and due date
    update-project --user --title    brings up interactive inputs to update
    remove-project --title
    view-projects [--user]
    
    add-task --project --title
    update-task --project --title    brings up interactive
    remove-task --project --title
    view-tasks --project
    
    summarize-project --project    
"""   

    
def main():
    """Entry point of program.
    Inside a global try/except block to provide basic formatting and catch errors gracefully."""
    try:
        pass
    except ValueError as err:
        print(f"[red]Input error:[/red] {err}")
    except TypeError as err:
        print(f"[red]Type error:[/red] {err}")
        print("[u][bold][red]REPORT THIS TO THE DEVELOPER![/u][/bold] This should never happen!")



if __name__ == "__main__":
    main()