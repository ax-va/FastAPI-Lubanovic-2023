INTEGRITY_ERROR_UNIQUE = "unique constraint failed"


class DuplicateError(Exception):
    pass


class NotFoundError(Exception):
    pass
