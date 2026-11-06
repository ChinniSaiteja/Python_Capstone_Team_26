"""
Subsystem: Backend & Application Integration
Home Assignment 1

GuidanceService
---------------
Coordinates access to disposal guidance and classification storage.

The actual SQL/database implementation remains inside DatabaseManager.
This class acts as an integration layer between the backend workflow
and the existing Data Management subsystem.
"""

from database.db import DatabaseManager


class GuidanceService:
    """Provide disposal guidance and store classification results."""

    DEFAULT_REGION = "Dortmund"

    # 1. Constructor
    def __init__(
        self,
        database_manager: DatabaseManager,
        default_region: str = DEFAULT_REGION,
    ):
        self.__database_manager = database_manager
        self.__default_region = default_region
        self.__initialized = False

    # 2. Initialisation method
    def initialize(self) -> None:
        """Initialise the guidance service and database."""
        self.__default_region = self.__default_region.strip().title()

        if not self.__default_region:
            raise ValueError("Default region must not be empty.")

        self.__database_manager.initialize()
        self.__initialized = True

    # 3. Getters and setters

    @property
    def database_manager(self) -> DatabaseManager:
        """Return the database manager."""
        return self.__database_manager

    @database_manager.setter
    def database_manager(self, value: DatabaseManager) -> None:
        """Set the database manager."""
        if not isinstance(value, DatabaseManager):
            raise TypeError("database_manager must be a DatabaseManager.")

        self.__database_manager = value

    @property
    def default_region(self) -> str:
        """Return the default region."""
        return self.__default_region

    @default_region.setter
    def default_region(self, value: str) -> None:
        """Set the default region."""
        value = str(value).strip().title()

        if not value:
            raise ValueError("Default region must not be empty.")

        self.__default_region = value

    @property
    def initialized(self) -> bool:
        """Return whether the service has been initialized."""
        return self.__initialized

    # 4. Guidance retrieval

    def get_guidance(
        self,
        label: str,
        region: str | None = None,
    ) -> dict | None:
        """
        Retrieve disposal guidance using the classifier label.

        Example:

            get_guidance("glass jar")

        Returns the disposal rule as a dictionary.
        """

        label = str(label).strip().lower()

        if not label:
            raise ValueError("Label must not be empty.")

        selected_region = (
            region.strip().title()
            if region
            else self.__default_region
        )

        return self.__database_manager.get_rule(
            label=label,
            region=selected_region,
        )

    # 5. Save classification

    def save_classification(
        self,
        label: str,
        confidence: float | None = None,
        status: str = "completed",
        region: str | None = None,
    ) -> int:
        """
        Save a classification result in the database.

        Returns the database classification ID.
        """

        selected_region = (
            region.strip().title()
            if region
            else self.__default_region
        )

        return self.__database_manager.save_classification(
            label=label,
            confidence=confidence,
            status=status,
            region=selected_region,
        )

    # 6. Process complete guidance request

    def process_classification(self, classification: dict) -> dict:
        """
        Retrieve guidance and save the classification.

        Expected input:

            {
                "label": "glass jar",
                "confidence": 0.92,
                "status": "completed",
                "region": "Dortmund"
            }

        Returns:

            {
                "guidance": {...},
                "classification_id": 1
            }
        """

        label = classification["label"]
        confidence = classification.get("confidence")
        status = classification.get("status", "completed")
        region = classification.get(
            "region",
            self.__default_region,
        )

        # Retrieve disposal guidance
        guidance = self.get_guidance(
            label=label,
            region=region,
        )

        # Save classification
        classification_id = self.save_classification(
            label=label,
            confidence=confidence,
            status=status,
            region=region,
        )

        return {
            "guidance": guidance,
            "classification_id": classification_id,
        }