#! /usr/bin/env python3

from rich import print
from rich.console import Console
from rich.table import Table
from src.models.user import User
from src.models.task import Task
from src.models.project import Project
from src.services.storage_service import Storage
from src.utils.logger import DualLogger
from src.globals import ENABLE_DEBUG_LOGGING
import argparse
import src.parser_functions as pf

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
# =========================== Globals ============================== #

"""File level logger object"""
logger = DualLogger("Main", "main.log", debug=ENABLE_DEBUG_LOGGING)

"""Arugument information that is used more than once."""
name_names = ("-n", "--name")
name_config = {"required": True, "help": "Name to give user."}
email_names = ("-e", "--email")
email_config = {"help": "User's email address."}
user_names = ("-u", "--user")
user_config = {"required": True, "help": "User's name."}
title_names = ("-t", "--title")
title_config = {"required": True, "help": "Title of project/task."}
project_names = ("-p", "--project")
project_config = {"required": True, "help": "Name of project."}
description_names = ("-d", "--description")
description_config = {"help": "Description of project."}
due_date_name = "--due_date"
due_date_config = {"help": "Date project is due."}




# =========================== Main ============================== #
def main():
    """Entry point of program.
    Inside a global try/except block to provide basic formatting and catch errors gracefully.
    """

    #  Primary parser objects
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers()

    # ================= User Parsers ================ #

    users_parser = subparsers.add_parser("users", help="Add and manage users.")
    users_subparsers = users_parser.add_subparsers()

    # ------- Add user ------- #
    add_user_parser = users_subparsers.add_parser("add", help="Add a new user.")
    add_user_parser.add_argument(*name_names, **name_config)
    add_user_parser.add_argument(*email_names, required=True, **email_config)
    add_user_parser.set_defaults(func=pf.add_user)

    # ------- Update user ------- #
    update_user_parser = users_subparsers.add_parser(
        "update", help="Update an existing user."
    )
    update_user_parser.add_argument(*name_names, **name_config)
    update_user_parser.add_argument("--new_name", help="New name for user.")
    update_user_parser.add_argument(*email_names, **email_config)
    update_user_parser.set_defaults(func=pf.update_user)

    # ------- Remove user ------- #
    remove_user_parser = users_subparsers.add_parser(
        "remove", help="Remove an existing user."
    )
    remove_user_parser.add_argument(*name_names, **name_config)
    remove_user_parser.set_defaults(func=pf.remove_user)

    # ------- List users ------- #
    list_user_parser = users_subparsers.add_parser("list", help="List all users.")
    list_user_parser.set_defaults(func=pf.list_users)

    # ================= Profile Parsers ================ #

    projects_parser = subparsers.add_parser("projects", help="Add and manage projects.")
    projects_subparsers = projects_parser.add_subparsers()

    # ------- Add project ------- #
    add_project_parser = projects_subparsers.add_parser(
        "add", help="Add a new project."
    )
    add_project_parser.add_argument(*user_names, **user_config)
    add_project_parser.add_argument(*title_names, **title_config)
    add_project_parser.add_argument(
        *description_names, required=True, **description_config
    )
    add_project_parser.add_argument(due_date_name, required=True, **due_date_config)
    add_project_parser.set_defaults(func=pf.add_project)

    # ------- Update project ------- #
    update_project_parser = projects_subparsers.add_parser("update", help="Update an existing project.")
    update_project_parser.add_argument(*user_names, **user_config)
    update_project_parser.add_argument(*title_names, **title_config)
    update_project_parser.add_argument("--new_title", help="New title for project.")
    update_project_parser.add_argument(*description_names, **description_config)
    update_project_parser.add_argument(due_date_name, **due_date_config)
    update_project_parser.set_defaults(func=pf.update_project)

    # ------- Remove project ------- #
    remove_project_parser = projects_subparsers.add_parser("remove", help="Remove an existing project.")
    remove_project_parser.add_argument(*user_names, **user_config)
    remove_project_parser.add_argument(*title_names, **title_config)
    remove_project_parser.set_defaults(func=pf.remove_project)

    # ------- List projects ------- #
    list_projects_parser = projects_subparsers.add_parser("list", help="List projects for given user.")
    # a little tacky cause it's the only place user isn't required, and I didn't want to hard code the string here.
    list_projects_parser.add_argument(*user_names, help=user_config["help"])
    list_projects_parser.set_defaults(func=pf.list_projects)

    # ================= Task Parsers ================ #

    # ================= Execution Point ================ #
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
