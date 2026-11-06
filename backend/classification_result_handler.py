"""
Subsystem: Backend & Application Integration
Home Assignment 1

ClassificationResultHandler
---------------------------
Handles and validates the prediction returned by the ML classifier.

The classifier is responsible for making the prediction.
This class is responsible for validating and normalising that result
before it is passed to the next backend component.
"""


class ClassificationResultHandler:
    """Validate and normalise a classifier prediction."""

    DEFAULT_REGION = "Dortmund"
    ALLOWED_STATUS = ("completed", "uncertain", "failed")

    # 1. Constructor
    def __init__(self, default_region: str = DEFAULT_REGION):
        self.__default_region = default_region
        self.__initialized = False

    # 2. Initialisation method
    def initialize(self) -> None:
        """Initialise the result handler."""
        self.__default_region = self.__default_region.strip().title()

        if not self.__default_region:
            raise ValueError("Default region must not be empty.")

        self.__initialized = True

    # 3. Getters and setters

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
        """Return whether the handler has been initialized."""
        return self.__initialized

    # 4. Main processing method

    def handle(self, prediction: dict) -> dict:
        """
        Validate and normalise the classifier result.

        Expected classifier input:

            {
                "label": "glass jar",
                "confidence": 0.92
            }

        Returns:

            {
                "label": "glass jar",
                "confidence": 0.92,
                "status": "completed",
                "region": "Dortmund"
            }
        """

        if not isinstance(prediction, dict):
            raise ValueError("Classifier prediction must be a dictionary.")

        label = prediction.get("label")
        confidence = prediction.get("confidence")

        # Validate label
        if label is None or not str(label).strip():
            raise ValueError("Classifier result must contain a non-empty label.")

        label = str(label).strip().lower()

        # Validate confidence if provided
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                raise ValueError("Confidence must be a number.") from None

            if not 0.0 <= confidence <= 1.0:
                raise ValueError("Confidence must be between 0 and 1.")

        # Determine status
        status = prediction.get("status", "completed")

        if status not in self.ALLOWED_STATUS:
            raise ValueError(
                f"Status must be one of {self.ALLOWED_STATUS}."
            )

        # Region can be supplied by the caller.
        # Otherwise Dortmund is used by default.
        region = prediction.get("region", self.__default_region)
        region = str(region).strip().title()

        if not region:
            raise ValueError("Region must not be empty.")

        return {
            "label": label,
            "confidence": confidence,
            "status": status,
            "region": region,
        }