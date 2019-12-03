from typing import Optional


class Logger:
    """This class centralises all log messages, and allows to easily change where these messages
    go to. The simplest implementation will just print the messages to the standard output."""
    def __init__(self, name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self.name = name or self.__class__.__name__

    def log(self, message: str):
        """Logs a message, formatting it with the name of the entity"""
        print(f"[{self.name}] {message}")
