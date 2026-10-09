from src.utils.logger import DualLogger
from src.globals import ENABLE_DEBUG_LOGGING

logger = DualLogger("Task", "task.log", debug=ENABLE_DEBUG_LOGGING)

class Task:
    """Task object that stores information about the task.
    
    Attributes:
        title (str): Title of the task.
        status (str): Status of the task.
        assigned_to (str): Name of the user this task is assigned to."""
    
    def __init__(self, title, status, assigned_to):
        """Initializes object.
        
        Args:
            title (str): Title of the task.
            status (str): Status of the task.
            assigned_to (str): Name of the user this task is assigned to."""
            
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
            logger.info(
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
            logger.info(
                f"Failed to add task status to task {self.title}: entry was empty."
            )
            raise ValueError("Task status cannot be blank.")
        self._status = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        """Assigns task to a name.
        Raises:
            ValueError: if no value is passed in."""
        if not value:
            logger.warn(
                f"Failed to assign user to {self.title}: Passed no value."
            )
            raise ValueError(
                f"Failed to assign user to {self.title}: No value was passed in."
            )

    def update_task(self, title, status, assigned_to):
        """Updates self.
        Returns:
            string delimited by |"""
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

        return str(self)
