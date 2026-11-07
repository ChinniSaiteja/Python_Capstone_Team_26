from Hometaskassignment3.exceptions import (
    WebInterfaceError,
    InvalidRequestError,
    DatabaseError,
    DatabaseConnectionError,
    DatabaseQueryError,
)


def test_invalid_request_error_inherits_from_web_interface_error():
    error = InvalidRequestError("Invalid request")
    assert isinstance(error, WebInterfaceError)


def test_database_connection_error_inherits_from_database_error():
    error = DatabaseConnectionError("Connection failed")
    assert isinstance(error, DatabaseError)


def test_database_query_error_inherits_from_database_error():
    error = DatabaseQueryError("Query failed")
    assert isinstance(error, DatabaseError)


def test_database_error_inherits_from_exception():
    error = DatabaseError("Database error")
    assert isinstance(error, Exception)