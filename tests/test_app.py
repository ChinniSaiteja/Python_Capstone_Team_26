from unittest.mock import patch

from Hometaskassignment3.app import app
from Hometaskassignment3.exceptions import DatabaseQueryError


def test_app_is_initialized():
    assert app is not None
    assert app.name == "Hometaskassignment3.app"


def test_home_route_exists():
    mock_items = []

    with patch(
        "Hometaskassignment3.app.get_waste_items",
        return_value=mock_items,
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 200


def test_home_page_displays_waste_items():
    mock_items = [
    {
        "id": 1,
        "item_name": "Plastic Bottle",
        "material": "Plastic",
        "disposal_method": "Plastic recycling bin",
    },
    {
        "id": 2,
        "item_name": "Glass Jar",
        "material": "Glass",
        "disposal_method": "Glass recycling container",
    },
]

    with patch(
        "Hometaskassignment3.app.get_waste_items",
        return_value=mock_items,
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 200
    assert b"Plastic Bottle" in response.data
    assert b"Glass Jar" in response.data
    assert b"Plastic" in response.data
    assert b"Glass" in response.data


def test_database_error_returns_500_error_page():
    with patch(
        "Hometaskassignment3.app.get_waste_items",
        side_effect=DatabaseQueryError("Query failed"),
    ):
        with app.test_client() as client:
            response = client.get("/")

    assert response.status_code == 500
    assert b"database service is currently unavailable" in response.data