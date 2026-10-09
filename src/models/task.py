from src.utils.logger import DualLogger
from main import ENABLE_DEBUG_LOGGING
from user import User


class Task:
    logger = DualLogger("Task", "task.log", debug=ENABLE_DEBUG_LOGGING)

    def __init__(self, title, status, assigned_to):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def __str__(self):
        """Formats string representation of self.
        Returns:
            String delimited with | for easier formatting in CLI."""
        return f"{self.title} | {self.status} | {self.assigned_to.name}"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        """Sets title.
        Raises:
            ValueError: if input empty"""
        if not value or not value.strip():
            self.logger.info(
                f"Failed to add task title {"to" + self.title if self.title else ""}: entry was empty."
            )
            raise ValueError("Task title cannot be blank.")
        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        """Sets status.
        Raises:
            ValueError if blank."""
        if not value or not value.strip():
            self.logger.info(
                f"Failed to add task status to task {self.title}: entry was empty."
            )
            raise ValueError("Task status cannot be blank.")
        self._status = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        """Assigns task based on User.
        Raises:
            TypeError: if value is not of type User."""
        if not value:
            self.logger.error(
                f"Failed to assign user to {self.title}: Passed no value."
            )
            raise TypeError(
                f"Failed to assign user to {self.title}: No value was passed in."
            )
        if not isinstance(value, User):
            self.logger.error(
                f"Failed to assign user to {self.title}: not a valid User object."
            )
            raise TypeError(
                f"Failed to assign user to {self.title}: not a valid User object."
            )

    def update_task(self, title, status, assigned_to):
        """Updates self.
        Returns:
            string delimited by |"""
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

        return str(self)
