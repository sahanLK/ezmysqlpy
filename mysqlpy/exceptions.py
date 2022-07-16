
class ServerConnectionError(Exception):
    def __init__(self, msg="Error when connecting to database server."):
        self.msg = msg

    def __str__(self):
        return self.msg


class DatabaseSelectionError(Exception):
    def __init__(self, msg="Database selection error."):
        self.msg = msg

    def __str__(self):
        return self.msg


class DatabaseCreateError(Exception):
    def __init__(self, msg="Error when creating database."):
        self.msg = msg

    def __str__(self):
        return self.msg


class DatabaseDropError(Exception):
    def __init__(self, msg="Error when deleting database."):
        self.msg = msg

    def __str__(self):
        return self.msg


class TableCreateError(Exception):
    def __init__(self, msg="Error when creating table."):
        self.msg = msg

    def __str__(self):
        return self.msg


class RecordAddingError(Exception):
    def __init__(self, msg="Error when inserting record."):
        self.msg = msg

    def __str__(self):
        return self.msg


class TableNotFoundError(Exception):
    def __init__(self, msg="Selected table does not exists."):
        self.msg = msg

    def __str__(self):
        return self.msg


class TableAccessError(Exception):
    def __init__(self, msg="Error when accessing table."):
        self.msg = msg

    def __str__(self):
        return self.msg


