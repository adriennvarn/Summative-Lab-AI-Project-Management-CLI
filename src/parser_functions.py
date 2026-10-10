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
try:
    users = storage.load_data()
except EOFError:
    users = []
except FileNotFoundError:
    users = []

# =========================== Functions for Parsers ============================== #
""" Functions to be executed by parsers """

# ===================== Utility Functions ==================== #


# TODO format
def find_user(name):
    user = next((user for user in users if user.name == name), None)
    if not user:
        msg = f"No user named {name} exists."
        logger.info(msg)
        raise ValueError(msg)
    return user


# TODO format
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


def find_task(project, title):
    if not type(project).__name__ == "Project":
        raise TypeError(f"find_task expected type Project but received {type(project)}")

    task = next((task for task in project.tasks if task.title == title), None)
    if not task:
        msg = f"Project {project.title} does not have a task named {title}."
        logger.info(msg)
        raise ValueError(msg)
    return task


# ===================== User Management ==================== #


# TODO format
def add_user(args):
    new_user = User(args.name, args.email)
    users.append(new_user)
    storage.store_data(users)
    print(f"\n[green]New User added:[/green]\n{new_user}\n")


# TODO: format
def update_user(args):
    user = find_user(args.name)
    user.name = (
        args.new_name.strip() if args.new_name and args.new_name.strip() else user.name
    )
    user.email = args.email.strip() if args.email and args.email.strip() else user.email
    storage.store_data(users)
    print(f"User updated:\n{user}")


# TODO: format
# TODO find all tasks containing user and remove assignment
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


# TODO format
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
def add_task(args):
    project = find_project(args.user, args.project)
    assigned_user = find_user(args.assigned_to)
    new_task = Task(args.title, args.status, assigned_user)
    project.tasks.append(new_task)
    storage.store_data(users)
    print(f"Task '{new_task.title} added to project {project.title}.'")


# TODO update, takes proj title status assigned_to
def update_task(args):
    project = find_project(args.user, args.project)
    task = find_task(project, args.title)
    try:
        assigned_to = find_user(args.assigned_to)
    except ValueError:
        assigned_to = None
    
    task.title = (
        args.title.strip()
        if args.title and args.title.strip()
        else task.title
    )
    task.status = (
        args.status.strip()
        if args.status and args.status.strip()
        else task.status
    )
    task.assigned_to = (
        assigned_to
        if assigned_to
        else task.assigned_to
    )
    storage.store_data(users)
    print(f"\nTask updated:\n{task}\n")


# TODO remove, takes proj title
def remove_task(args):
    project = find_project(args.user, args.project)
    if not project.tasks:
        print(f"Project {project.title} has no tasks.")
    else:
        task = find_task(project, args.title)
        project.tasks.remove(task)
        print(f"Task {task.title} removed from {project.title}.")
        storage.store_data(users)


# TODO list, takes proj
def list_tasks(args):
    project = find_project(args.user, args.project)
    if not project.tasks:
        print(f"Project {project.title} has no tasks.")
    else:
        print(f"Tasks for project {project.title}:\n")
        for task in project.tasks:
            print(task)
        print()


# ===================== AI Summary ==================== #


# TODO summarize, takes proj
def summarize(args):
    pass
