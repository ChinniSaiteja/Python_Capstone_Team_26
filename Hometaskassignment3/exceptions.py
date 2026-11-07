class WebInterfaceError(Exception):
    """Base exception for web interface errors."""
    pass


class InvalidRequestError(WebInterfaceError):
    """Raised when a web request is invalid."""
    pass


class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when the database connection fails."""
    pass


class DatabaseQueryError(DatabaseError):
    """Raised when a database query fails."""
    pass