from src.services.storage_service import Storage
from rich import print
from src.models.user import User
from src.models.task import Task
from src.models.project import Project
from src.services.storage_service import Storage
from src.utils.logger import DualLogger
from src.services.ai_client import AIClient
from src.globals import ENABLE_DEBUG_LOGGING

logger = DualLogger(
    "Parser Functions", "parser_functions.log", debug=ENABLE_DEBUG_LOGGING
)

"""Global list of db"""
storage = Storage("db")

# if data can't be loaded, default to empty db
try:
    db = storage.load_data()
except EOFError:
    db = []
except FileNotFoundError:
    db = []

# =========================== Functions for Parsers ============================== #
""" Functions to be executed by parsers """

# ===================== Utility Functions ==================== #


# TODO format
def find_user(name):
    """Finds user from provided name.
    Args:
        name (str): Name assigned to user.
    Returns:
        User
    Raises:
        ValueError: If no user by that name exists"""

    user = next((user for user in db if user.name == name), None)
    if not user:
        msg = f"No user named {name} exists."
        logger.info(msg)
        raise ValueError(msg)
    return user


# TODO format
def find_project(name, title):
    """Finds project from provided user's name and project title.
    Args:
        name (str): name of user
        title (str): name of project
    Returns:
        Project
    Raises:
        ValueError: if no project found under that user"""

    user = find_user(name)
    project = next(
        (project for project in user.projects if project.title == title), None
    )
    if not project:
        msg = f"User {user.name} does not have a project named {title}."
        logger.info(msg)
        raise ValueError(msg)
    return project


# TODO format
def find_task(project, title):
    """Finds task given a project and task title.
    Args:
        project (Project): project to look for task under
        title (str): title of task
    Returns:
        Task
    Raises:
        TypeError: if project passed in is not of type Project
        ValueError: if no task found under that project"""

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
    """Adds user to db
    Args:
        name (str): name of new user
        email (str): email address for new user"""

    new_user = User(args.name, args.email)
    db.append(new_user)
    storage.store_data(db)
    print(f"\n[green]New User added:[/green]\n{new_user}\n")


# TODO format
def update_user(args):
    """Updates existing user in db
    Args:
        name (str): Name of user to update
        new_name (str): Optional, new name to assign user
        email (str): Optional, new email to assign user"""

    user = find_user(args.name)
    user.name = (
        args.new_name.strip() if args.new_name and args.new_name.strip() else user.name
    )
    user.email = args.email.strip() if args.email and args.email.strip() else user.email
    storage.store_data(db)
    print(f"User updated:\n{user}")


# TODO format
# TODO find all tasks containing user and remove assignment
def remove_user(args):
    user = find_user(args.name)
    db.remove(user)
    storage.store_data(db)
    print(f"User {args.name} removed.")


# TODO: format as table
def list_users(_):
    """Lists all users in db."""
    for user in db:
        print(user)


# ===================== Project Management ==================== #


# TODO format
def add_project(args):
    """Adds a project to a given user.
    Args:
        user (str): name of user to assign project to
        title (str): title of project
        despcription (str): description of project
        due_date (str): due date of project"""

    user = find_user(args.user)
    new_project = Project(args.title, args.description, args.due_date)
    user.add_project(new_project)
    storage.store_data(db)
    print(f"\n[green]Project added to {user.name}'s profile:[/green]\n{new_project}\n")


# TODO format
def update_project(args):
    """Updates existing project for given user
    Args:
        user (str): name of user project belongs to
        title (str): title of project to update
        new_title (str): Optional, new title to assign project
        description (str): Optional, new description to give project
        due_date (str): Optional, new due date for project"""

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
    storage.store_data(db)
    print(f"\nProject updated:\n{project}\n")


# TODO format
def remove_project(args):
    """Remove existing project for given user.
    Args:
        user (str): name of user owning profile
        title (str): title of project to remove"""

    user = find_user(args.user)
    project = find_project(args.user, args.title)
    user.projects.remove(project)
    storage.store_data(db)
    print(f"Project {project.title} removed from {user.name}'s profile.")


# TODO format
def list_projects(args):
    """Lists all projects for a given user, or all projects in db grouped by user.
    Args:
        user (str): Optional, name of user to list projects of"""

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
        for user in db:
            print_all(user)


# ===================== Task Management ==================== #


# TODO format
def add_task(args):
    """Add task to given user's project.
    Args:
        user (str): name of user that owns project
        project (str): title of project to add task to
        title (str): title of task
        status (str): status of task
        assigned_to (str): name of user to assign to task.
            doesn't have to be user owning project, but does have to exist in user db"""

    project = find_project(args.user, args.project)
    assigned_user = find_user(args.assigned_to)
    new_task = Task(args.title, args.status, assigned_user)
    project.tasks.append(new_task)
    storage.store_data(db)
    print(f"Task '{new_task.title} added to project {project.title}.'")


# TODO format
def update_task(args):
    """Update existing task for a given user's project.
    Args:
        user (str): name of user owning project
        project (str): title of project owning task
        title (str): current title of project
        new_title (str): Optional, new title for task
        status (str): Optional, new status to assign task
        assigned_to (str): Optional, name of user to reassign task to"""

    project = find_project(args.user, args.project)
    task = find_task(project, args.title)
    try:
        assigned_to = find_user(args.assigned_to)
    except ValueError:
        assigned_to = None

    task.title = (
        args.new_title.strip()
        if args.new_title and args.new_title.strip()
        else task.title
    )
    task.status = (
        args.status.strip() if args.status and args.status.strip() else task.status
    )
    task.assigned_to = assigned_to if assigned_to else task.assigned_to
    storage.store_data(db)
    print(f"\nTask updated:\n{task}\n")


# TODO format
def remove_task(args):
    """Remove existing task from a given user's project.
    Args:
        user (str): name of user owning project
        project (str): title of project owning task
        title (str): title of task to remove"""

    project = find_project(args.user, args.project)
    if not project.tasks:
        print(f"Project {project.title} has no tasks.")
    else:
        task = find_task(project, args.title)
        project.tasks.remove(task)
        print(f"Task {task.title} removed from {project.title}.")
        storage.store_data(db)


# TODO format
def list_tasks(args):
    """List all tasks for a given project.
    Args:
        user (str): name of user owning project
        project (str): title of project owning tasks to list"""

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
    """AI Summary of a given project.
    Args:
        user (str): name of user owning project
        project (str): name of project to summarize"""

    project = find_project(args.user, args.project)
    ai_client = AIClient()

    # pre-formatted prompt
    prompt = f"""
        Summarize the following project in one paragraph. Do not invent unsupported details. The response can be shorter than one paragraph if there is not enough information. 
        The project belongs to {args.user}. The title of the project is "{project.title}". The description of the project is "{project.description}". The due date of the project is "{project.due_date}".
        The project contains the following tasks:
        {"".join([f"\nTask: {task.title} | Status: {task.status} | Assigned to: {task.assigned_to.name}" for task in project.tasks])}
    """

    # Loading indicator
    print(
        f"[yellow]The AI is working on your summary. This can take a few moments, so please be patient![/yellow]"
    )

    # Get and print response
    response = ai_client.generate_response(prompt)
    print(f"AI Summary: {response}")

    # Clear history immediately, as each response should be generated freshly.
    ai_client.clear_history()
