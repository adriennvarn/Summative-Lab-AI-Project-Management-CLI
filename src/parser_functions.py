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

logger = DualLogger(
    "Parser Functions", "parser_functions.log", debug=ENABLE_DEBUG_LOGGING
)

"""Global list of users"""
storage = Storage("db")
users = storage.load_data()

# =========================== Functions for Parsers ============================== #
""" Functions to be executed by parsers """

# ===================== Utility Functions ==================== #


def find_user(name):
    user = next((user for user in users if user.name == name), None)
    if not user:
        msg = f"No user named {name} exists."
        logger.info(msg)
        raise ValueError(msg)
    return user


def find_project(username, title):
    user = find_user(username)
    project = next(
        (project for project in user.projects if project.title == title), None
    )
    if not project:
        msg = f"User {user.name} does not have a project named {title}."
        logger.info(msg)
        raise ValueError(msg)
    return project


# ===================== User Management ==================== #


def add_user(args):
    new_user = User(args.name, args.email)
    users.append(new_user)
    storage.store_data(users)
    print(f"\n[green]New User added:[/green]\n{new_user}\n")


def update_user(args):
    user = find_user(args.name)
    user.name = (
        args.new_name.strip() if args.new_name and args.new_name.strip() else user.name
    )
    user.email = args.email.strip() if args.email and args.email.strip() else user.email
    storage.store_data(users)
    print(f"User updated:\n{user}")


# TODO: format
def remove_user(args):
    user = find_user(args.name)
    users.remove(user)
    storage.store_data(users)
    print(f"User {args.name} removed.")


# TODO: format as table
def list_users(_):
    for user in users:
        print(user)


# ===================== Project Management ==================== #


def add_project(args):
    user = find_user(args.user)
    new_project = Project(args.title, args.description, args.due_date)
    user.add_project(new_project)
    storage.store_data(users)
    print(f"\n[green]Project added to {user.name}'s profile:[/green]\n{new_project}\n")


# TODO format
def update_project(args):
    project = find_project(args.user, args.title)
    project.title = (
        args.new_title.strip()
        if args.new_title and args.new_title.strip()
        else project.title
    )
    project.description = (
        args.description.strip()
        if args.description and args.description.strip()
        else project.description
    )
    project.due_date = (
        args.due_date.strip()
        if args.due_date and args.due_date.strip()
        else project.due_date
    )
    storage.store_data(users)
    print(f"\nProject updated:\n{project}\n")


# TODO format
def remove_project(args):
    user = find_user(args.user)
    project = find_project(args.user, args.title)
    user.projects.remove(project)
    storage.store_data(users)
    print(f"Project {project.title} removed from {user.name}'s profile.")


# TODO format
def list_projects(args):
    #  Print utility to be used with or without for loop
    def print_all(user):
        if user.projects:
            print(f"\n{user.name}'s Projects:")
            for project in user.projects:
                print(project)
            print()
        elif args.user and args.user.strip():
            print(f"User {user.name} has no projects.")
        
    #  if user provided, print only that one
    #  otherwise, print all
    if args.user and args.user.strip():
        user = find_user(args.user)
        print_all(user)
    else:
        for user in users:
            print_all(user)


# ===================== Task Management ==================== #

# TODO add, takes proj title status assigned_to

# TODO update, takes proj title status assigned_to

# TODO remove, takes proj title

# TODO list, takes proj


# ===================== AI Summary ==================== #

# TODO summarize, takes proj
