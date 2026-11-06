"""
Subsystem: Backend & Application Integration
Home Assignment 1

ResponseComposer
----------------
Creates a consistent response structure for the web interface.

This class does not communicate with the database, classifier,
or OpenAI API. It only combines already processed backend results.
"""


class ResponseComposer:
    """Compose the final response returned by the backend."""

    API_VERSION = "v1"

    # 1. Constructor
    def __init__(self, api_version: str = API_VERSION):
        self.__api_version = api_version
        self.__initialized = False

    # 2. Initialisation method
    def initialize(self) -> None:
        """Initialise the response composer."""
        self.__api_version = str(self.__api_version).strip()

        if not self.__api_version:
            raise ValueError("API version must not be empty.")

        self.__initialized = True

    # 3. Getters and setters

    @property
    def api_version(self) -> str:
        """Return the API version."""
        return self.__api_version

    @api_version.setter
    def api_version(self, value: str) -> None:
        """Set the API version."""
        value = str(value).strip()

        if not value:
            raise ValueError("API version must not be empty.")

        self.__api_version = value

    @property
    def initialized(self) -> bool:
        """Return whether the composer has been initialized."""
        return self.__initialized

    # 4. Response composition

    def compose(
        self,
        classification: dict,
        guidance: dict | None,
        classification_id: int | None = None,
    ) -> dict:
        """
        Create the final response for the frontend.

        Example output:

            {
                "api_version": "v1",
                "status": "completed",
                "classification": {
                    "label": "glass jar",
                    "confidence": 0.92
                },
                "disposal": {
                    ...
                },
                "classification_id": 1
            }
        """

        if not isinstance(classification, dict):
            raise ValueError("Classification must be a dictionary.")

        label = classification.get("label")

        if not label:
            raise ValueError("Classification must contain a label.")

        return {
            "api_version": self.__api_version,
            "status": classification.get("status", "completed"),
            "classification": {
                "label": label,
                "confidence": classification.get("confidence"),
                "region": classification.get(
                    "region",
                    "Dortmund",
                ),
            },
            "disposal": guidance,
            "classification_id": classification_id,
        }