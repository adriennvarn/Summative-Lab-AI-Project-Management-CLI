import ollama


class AIClient:
    """
    Reusable threaded client for interacting with local Ollama model.
    """

    def __init__(self, model="llama3.2"):
        """Initialize AI client.
        Args:
            model (str): ollama model to use. Defaults to llama3.2"""
        self.model_name = model
        self.messages = []

    def generate_response(self, prompt):
        """Generate a response to user prompt.
        Args:
            prompt (str): Prompt to feed the AI
        Returns:
            String containing content of AI's response.
        Raises:
            ValueError: if prompt is empty
            RuntimeError: if any other exception is raised"""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        user_message = {
            "role": "user",
            "content": prompt.strip(),
        }

        self.messages.append(user_message)

        try:
            response = ollama.chat(model=self.model_name, messages=self.messages)

            assistant_message = response["message"]
            self.messages.append(assistant_message)

            return assistant_message["content"]

        except Exception as err:
            self.messages.pop()
            raise RuntimeError(f"AI service request failed: {err}")

    def clear_history(self):
        """Erase conversation history."""
        self.messages = []

    def get_history(self):
        """Return a copy of conversation history."""
        return self.messages.copy()