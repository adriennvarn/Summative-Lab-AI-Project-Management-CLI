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

"""File level logger object"""
logger = DualLogger("Main", "main.log", debug=ENABLE_DEBUG_LOGGING)

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
storage = Storage("db")
users = storage.load_data()

"""Functions to be executed by parsers"""

""" User management """


def find_user(name):
    return next((user for user in users if user.name == name), None)


def add_user(args):
    new_user = User(args.name, args.email)
    users.append(new_user)
    storage.store_data(users)
    print(f"\n[green]New User added:[/green]\n{new_user}\n")


def update_user(args):
    # TODO: cope with no user found
    user = find_user(args.name)
    user.name = args.new_name if args.new_name and args.new_name.strip() else user.name
    user.email = args.email if args.email and args.email.strip() else user.email
    storage.store_data(users)
    print(f"User updated:\n{user}")


# TODO: format
def remove_user(args):
    user = find_user(args.name)
    if user:
        users.remove(user)
        storage.store_data(users)
        print(f"User {args.name} removed.")
    else:
        msg = f"Failed to remove user {args.name}: Does not exist."
        logger.info(msg)
        raise ValueError(msg)


# TODO: format as table
def list_users(_):
    for user in users:
        print(user)


""" Project Management """


def find_project(user, title):
    return next(
        (
            user.project
            for user in users
            if title in [project.title for project in user.projects]
        ),
        None,
    )


def add_project(args):
    new_project = Project(args.title, args.description, args.due_date)


def main():
    """Entry point of program.
    Inside a global try/except block to provide basic formatting and catch errors gracefully.
    """

    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers()

    """User management parsers"""

    users_parser = subparsers.add_parser("users", help="Add and manage users.")
    users_subparsers = users_parser.add_subparsers()

    # Add user
    add_user_parser = users_subparsers.add_parser("add", help="Add a new user.")
    add_user_parser.add_argument(*name_names, **name_config)
    add_user_parser.add_argument(
        "-e", "--email", required=True, help="User's email address."
    )
    add_user_parser.set_defaults(func=add_user)

    # Update user
    update_user_parser = users_subparsers.add_parser(
        "update", help="Update an existing user."
    )
    update_user_parser.add_argument(*name_names, **name_config)
    update_user_parser.add_argument(
        "--new_name", help="New name for user."
    )
    update_user_parser.add_argument(
        "-e", "--email", help="User's email address."
    )
    update_user_parser.set_defaults(func=update_user)

    # Remove user
    remove_user_parser = users_subparsers.add_parser(
        "remove", help="Remove an existing user."
    )
    remove_user_parser.add_argument(*name_names, **name_config)
    remove_user_parser.set_defaults(func=remove_user)

    # List users
    list_user_parser = users_subparsers.add_parser("list", help="List all users.")
    list_user_parser.set_defaults(func=list_users)

    """Project management parsers"""

    projects_parser = subparsers.add_parser("projects", help="Add and manage projects.")
    projects_subparsers = projects_parser.add_subparsers()

    # Add project
    add_project_parser = projects_subparsers.add_parser(
        "add", help="Add a new project."
    )
    add_project_parser.add_argument(*user_names, **user_config)
    add_project_parser.add_argument(*title_names, **title_config)
    add_project_parser.add_argument("-d", help="tbc")
    add_project_parser.set_defaults(func=add_project)

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
