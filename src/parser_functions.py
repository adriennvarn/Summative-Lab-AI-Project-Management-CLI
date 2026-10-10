from src.services.storage_service import Storage
from rich import print
from rich.console import Console
from rich.table import Table
from src.models.user import User
from src.models.task import Task
from src.models.project import Project
from src.services.storage_service import Storage
from src.utils.logger import DualLogger
from src.globals import ENABLE_DEBUG_LOGGING

logger = DualLogger("Parser Functions", "parser_functions.log", debug=ENABLE_DEBUG_LOGGING)

"""Global list of users"""
storage = Storage("db")
users = storage.load_data()

# =========================== Functions for Parsers ============================== #
""" Functions to be executed by parsers """

# ===================== Utility Functions ==================== #


def find_user(name):
    return next((user for user in users if user.name == name), None)


def find_project(username, title):
    user = find_user(username)
    return next((project for project in user.projects if project.title == title), None)


# ===================== User Management ==================== #


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


# ===================== Project Management ==================== #


def add_project(args):
    user = find_user(args.user)
    if not user:
        msg = f"No user named {args.user} exists."
        logger.info(msg)
        raise ValueError(msg)

    new_project = Project(args.title, args.description, args.due_date)
    user.add_project(new_project)
    storage.store_data(users)
    print(f"\n[green]Project added to {user.name}'s profile:[/green]\n{new_project}\n")
    
# TODO update

# TODO remove

# TODO format
def list_projects(args):
    if args.user and args.user.strip():
        user = find_user(args.user)
        if not user:
            msg = f"No user named {args.user} exists."
            logger.info(f"Failed to list projects: {msg}")
            raise ValueError(msg)

        for project in user.projects:
            print(project)

    else:
        for user in users:
            if user.projects:
                print(f"\n{user.name}'s Projects:")
                for project in user.projects:
                    print(project)
                print()

# ===================== Task Management ==================== #

# TODO add, takes proj title status assigned_to

# TODO update, takes proj title status assigned_to

# TODO remove, takes proj title

# TODO list, takes proj


# ===================== AI Summary ==================== #

# TODO summarize, takes proj
