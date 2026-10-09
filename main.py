#! /usr/bin/env python3

from rich import print
from src.models.user import User
from src.models.task import Task
from src.models.project import Project
from src.services.storage_service import Storage
import argparse


"""
cmds:
    -n, --name
    -e, --email
    -u, --user
    -t, --title
    -d, --description
    -p, --project

    add-user --name --email
    update-user --name               brings up interactive, update name and/or email
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

"""Arugument information that is used more than once."""
name_names = ("-n", "--name")
name_config = {"required": True, "help": "Name to give user."}
user_names = ("-u", "--user")
user_config = {"required": True, "help": "User's name."}
title_names = ("-t", "--title")
title_config = {"required": True, "help": "Title of project/task."}
project_names = ("-p", "--project")
project_config = {"required": True, "help": "Name of project."}

"""Global list of users"""
users = []
storage = Storage("db.json")

"""Functions to be executed by parsers"""

"""User management"""


def add_user(args):
    new_user = User(args.name, args.email)
    users.append(new_user)
    storage.store_data(users)
    print(f"\n[green]New User added:[/green]\n{new_user}\n")


def main():
    """Entry point of program.
    Inside a global try/except block to provide basic formatting and catch errors gracefully.
    """

    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers()

    """User management parsers"""
    # Add user
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user.")
    add_user_parser.add_argument(*name_names, **name_config)
    add_user_parser.add_argument("-e", "--email", required=True, help="User's email address.")
    add_user_parser.set_defaults(func=add_user)
    
    

    try:
        args = parser.parse_args()

        # handle missing command
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
    except ValueError as err:
        print(f"[red]Input error:[/red] {err}")
    except TypeError as err:
        # Report serious error and abort program.
        print(f"[red]Type error:[/red] {err}")
        print(
            "[u][bold][red]REPORT THIS TO THE DEVELOPER![/u][/bold] This should never happen!"
        )
    except Exception as err:
        # Report serious error and abort program.
        print(f"[red]Unknown error:[/red] {err}")
        print(
            "[u][bold][red]REPORT THIS TO THE DEVELOPER![/u][/bold] This should never happen!"
        )


if __name__ == "__main__":
    main()
