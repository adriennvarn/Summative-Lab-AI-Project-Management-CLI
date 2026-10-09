from src.utils.logger import DualLogger
from main import ENABLE_DEBUG_LOGGING
from task import Task
from rich import print


class Project:
    """
    Project object, containing information about project and a list of tasks.

    Attributes:
        title (str): Title of project.
        description (str): Description of project.
        due_date (str): Due date as string.

    Note:
        due_date remains a plain string as date manipulation is not required here.
    """

    logger = DualLogger("Project", "project.log", debug=ENABLE_DEBUG_LOGGING)

    def __init__(self, title, description, due_date):
        """Initializes project with information and empty task list.

        Args:
            title (str): Title of project.
            description (str): Description of project.
            due_date (str): Due date as string.
        """

        self.title = title
        self.description = description
        self.due_date = due_date

        self.tasks = []

    def __str__(self):
        """Formats string representation.
        Returns:
            Fields delimited by | for easier formatting in CLI."""
        return f"{self.title} | {self.description} | {self.due_date}"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        """Sets title.
        Raises:
            ValueError: if empty."""

        if not value or not value.strip():
            self.logger.info(
                f"Title for {"project" + self.title if self.title else "new project"} was empty."
            )
            raise ValueError("Title must not be blank.")

        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        """Sets description.
        Raises:
            ValueError: if empty."""

        if not value or not value.strip():
            self.logger.info(f"Description for {self.title} was empty.")
            raise ValueError("Description must not be blank.")

        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        """Sets due date. Saved as standard string since date manipulation is not required.
        Raises:
            ValueError: if empty."""

        if not value or not value.strip():
            self.logger.info(f"Due date for {self.title} was empty.")
            raise ValueError("Due date must not be blank.")

        self._due_date = value

    def update_project(self, title, description, due_date):
        """Updates self.
        Returns:
            String with fields delimited by |"""

        self.title = title
        self.description = description
        self.due_date = due_date

        return str(self)

    def add_task(self, task):
        """Adds task to project task list.
        Raises:
            TypeError: if task is not of type Task"""

        if not isinstance(task, Task):
            self.logger.error(
                f"Adding task to project {self.title} failed: task was of type {type(task)}"
            )
            raise TypeError(
                f"Attempted to add task of type {type(task)}, which is not valid."
            )

        self.tasks.append(task)

    def remove_task(self, task_to_remove):
        """Removes task by title from project task list..
        Raises:
            ValueError: if task title is not in task list, or title is empty."""

        if not task_to_remove or not task_to_remove.strip():
            self.logger.warn(
                f"Tried to remove task from {self.title} but input was empty."
            )
            raise ValueError(f"Task title cannot be blank.")

        try:
            self.tasks.remove(
                next(task for task in self.tasks if task.title == task_to_remove), None
            )
            return f"Task {task_to_remove} was successfully removed."
        except ValueError as err:
            self.logger.info(
                f"No task by name {task_to_remove} found in task list of {self.title}."
            )
            raise ValueError(
                f"There is no task named '{task_to_remove}' for project {self.title}."
            )
