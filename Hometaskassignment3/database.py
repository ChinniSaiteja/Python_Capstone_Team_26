import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# from exceptions import DatabaseConnectionError, DatabaseQueryError
from Hometaskassignment3.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
)

load_dotenv(Path(__file__).resolve().parent / ".env")


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return connection

    except mysql.connector.Error as error:
        raise DatabaseConnectionError(
            "Unable to connect to the database."
        ) from error


def get_waste_items():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM waste_items")
        items = cursor.fetchall()

        return items

    except DatabaseConnectionError:
        raise

    except mysql.connector.Error as error:
        raise DatabaseQueryError(
            "Unable to retrieve waste items from the database."
        ) from error

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()