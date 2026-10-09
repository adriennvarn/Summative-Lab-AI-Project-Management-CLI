from src.utils.logger import DualLogger
from src.globals import ENABLE_DEBUG_LOGGING
import json

logger = DualLogger("Storage Service", "storage.log", debug=ENABLE_DEBUG_LOGGING)

class Storage:
    """Storage utility class.
    Stores a class level filepath to be accessed with only a single instatiation.
    
    Attributes:
        filepath (str): Path to the desired file to store and retrieve data."""
    
    filepath = ""
    
    def __init__(self, filepath):
        """Initializes class attribute with filepath.
        Args:
            filepath (str): Path to desired file. .json ending optional."""
        if not filepath or not filepath.strip():
            raise RuntimeError("Filepath must not be empty.")
        if not filepath.endswith(".json"):
            Storage.filepath = f"{filepath}.json"
        else:
            Storage.filepath = filepath
    
    @classmethod
    def store_data(cls, data):
        """Takes data and JSON-ifies it, before storing it in existing file path.
        Args:
            data (any): Data to be written to file.
            
        Returns:
            string: Confirmation message if successfull
            
            TODO: FIX EXCEPTIONS"""
        
        try:
            with open(cls.filepath, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as err:
            raise Exception("Error in storage_service write:" + err)
        
        return f"Data successfully saved to {cls.filepath}"
    
    @classmethod
    def load_data(cls):
        """Reads JSON data from class filepath.
        
        Returns:
            data retrieved from JSON file
        
        Raises:
            RuntimeError: if JSON cannot be parsed
            FileNotFoundError: if file cannot be found at filepath"""
            
        try:
            with open(cls.filepath, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError as err:
            msg = f"File not found at {cls.filepath}"
            logger.error(msg)
            raise FileNotFoundError(msg)
        except json.JSONDecodeError as err:
            msg = f"Error loading JSON from {cls.filepath}: {err}"
            logger.error(msg)
            raise RuntimeError(msg)