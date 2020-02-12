class Database:
    """A sample Employee class"""

    def __init__(self, need, command, complete,completed):
        self.need = need
        self.command = command
        self.complete = complete
        self.completed = completed

    @property
    def user_one(self):
        return '{} {}'.format(self.need, self.command)
