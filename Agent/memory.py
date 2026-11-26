from google.genai import types

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, text):
        self.history.append(
            types.Content(
                role="user",
                parts=[types.Part(text=text)]
            )
        )

    def add_model_message(self, text):
        self.history.append(
            types.Content(
                role="model",
                parts=[types.Part(text=text)]
            )
        )

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()