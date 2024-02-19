class NotEnoughStorage(Exception):
    def __init__(self, message="not enogh storage in this account"):
            self.message = message
            super().__init__(self.message)


class Completed(Exception):
    def __init__(self, message="Completed"):
        self.message = message
        super().__init__(self.message)
class Conflict(Exception):
    def __init__(self, message="Conflict"):
        self.message = message
        super().__init__(self.message)
class Failed(Exception):
    def __init__(self, message="Failed"):
        self.message = message
        super().__init__(self.message)
class FileNotFound(Exception):
    def __init__(self, message="File not found in accounts.json"):
        self.message = message
        super().__init__(self.message)
class FolderNotFound(Exception):
    def __init__(self, message="Folder not found in this account"):
        self.message = message
        super().__init__(self.message)
