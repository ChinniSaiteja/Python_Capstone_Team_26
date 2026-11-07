from unittest.mock import MagicMock, patch

import mysql.connector
import pytest

from Hometaskassignment3.database import (
    get_db_connection,
    get_waste_items,
)
from Hometaskassignment3.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
)


def test_get_db_connection_success():
    mock_connection = MagicMock()

    with patch(
        "Hometaskassignment3.database.mysql.connector.connect",
        return_value=mock_connection,
    ):
        connection = get_db_connection()

    assert connection == mock_connection


def test_get_db_connection_failure():
    with patch(
        "Hometaskassignment3.database.mysql.connector.connect",
        side_effect=mysql.connector.Error("Connection failed"),
    ):
        with pytest.raises(DatabaseConnectionError):
            get_db_connection()


def test_get_waste_items_success():
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "name": "Plastic"},
        {"id": 2, "name": "Paper"},
    ]

    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    with patch(
        "Hometaskassignment3.database.get_db_connection",
        return_value=mock_connection,
    ):
        items = get_waste_items()

    assert len(items) == 2
    assert items[0]["name"] == "Plastic"
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM waste_items"
    )


def test_get_waste_items_query_failure():
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = mysql.connector.Error(
        "Query failed"
    )

    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    with patch(
        "Hometaskassignment3.database.get_db_connection",
        return_value=mock_connection,
    ):
        with pytest.raises(DatabaseQueryError):
            get_waste_items()