class NotInitializedException(Exception):
    def __init__(self):
        super().__init__("Session is not initialized")
