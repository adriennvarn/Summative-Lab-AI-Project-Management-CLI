import re
from src.globals import ENABLE_DEBUG_LOGGING
from src.utils.logger import DualLogger

logger = DualLogger("User", "user.log", debug=ENABLE_DEBUG_LOGGING)

class User:
    """User object containing information about user and a list of projects.
    
    Attributes:
        name (str): Name of user.
        email (str): Email address of user.
        projects (list): List of Project objects owned by user."""

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []

    def __str__(self):
        """Formats string representation.
        Returns:
            Fields delimited by | for easier formatting in CLI."""

        return f"{self.name} | {self.email}"

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """Set email.
        Raises:
            ValueError: if email address is invalid.
        """
        #  use regex to check email validity
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            self._email = value
        else:
            raise ValueError(
                "Email must be a valid email address in the format [u]user@domain.com[/u]"
            )

    def update_user(self, name, email):
        """Updates self with new name and email.
        Verifies name isn't empty. Email validated as property.
        Raises:
            ValueError: if name is blank"""

        if not name or not name.strip():
            logger.info(f"Could not update user {self.name}: entry was empty.")
            raise ValueError("Name cannot be blank.")

        self.name = name
        self.email = email

    def add_project(self, project):
        """
        Adds a project object to user's project list.
        Raises:
            TypeError: if object is not of type Project
        """

        if not type(project).__name__ == "Project":
            msg = f"Expected type Project but received type {type(project)}"
            logger.error(msg)
            raise TypeError(msg)
