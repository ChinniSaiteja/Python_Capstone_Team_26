from unittest.mock import patch

from Hometaskassignment3.app import app
from Hometaskassignment3.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
)


def test_database_connection_error_is_handled_by_flask():
    with patch(
        "Hometaskassignment3.app.get_waste_items",
        side_effect=DatabaseConnectionError("Connection failed"),
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 500
    assert b"database service is currently unavailable" in response.data


def test_database_query_error_is_handled_by_flask():
    with patch(
        "Hometaskassignment3.app.get_waste_items",
        side_effect=DatabaseQueryError("Query failed"),
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 500
    assert b"database service is currently unavailable" in response.data


def test_unexpected_error_is_handled_by_flask():
    with patch(
        "Hometaskassignment3.app.get_waste_items",
        side_effect=RuntimeError("Unexpected failure"),
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 500
    assert b"An unexpected error occurred." in response.data