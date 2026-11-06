"""
Home Assignment 1 - Unit and integration tests
Subsystem: Backend & Application Integration

Tests:
    1. ClassificationResultHandler
    2. GuidanceService
    3. ResponseComposer

The tests use a temporary SQLite database, so they do not modify
the project's real database/waste.db file.
"""

import pytest

from backend.classification_result_handler import ClassificationResultHandler
from backend.guidance_service import GuidanceService
from backend.response_composer import ResponseComposer
from database.db import DatabaseManager


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    """
    Create a fresh temporary SQLite database for every test.

    The existing DatabaseManager is responsible for creating
    the tables and loading the Dortmund disposal rules.
    """
    manager = DatabaseManager(
        engine="sqlite",
        db_path=str(tmp_path / "test_backend.db"),
    )

    manager.initialize()

    return manager


@pytest.fixture
def result_handler():
    """Create and initialise the classification result handler."""
    handler = ClassificationResultHandler(
        default_region="Dortmund"
    )
    handler.initialize()

    return handler


@pytest.fixture
def guidance_service(db):
    """Create and initialise the guidance service."""
    service = GuidanceService(
        database_manager=db,
        default_region="Dortmund",
    )
    service.initialize()

    return service


@pytest.fixture
def response_composer():
    """Create and initialise the response composer."""
    composer = ResponseComposer(api_version="v1")
    composer.initialize()

    return composer


# ------------------------------------------------------------------
# ClassificationResultHandler tests
# ------------------------------------------------------------------

def test_classification_result_handler_normalises_prediction(
    result_handler,
):
    """
    The handler should normalise the classifier output.

    Example:
        'Glass Jar' -> 'glass jar'
    """

    prediction = {
        "label": "Glass Jar",
        "confidence": 0.92,
    }

    result = result_handler.handle(prediction)

    assert result["label"] == "glass jar"
    assert result["confidence"] == 0.92
    assert result["status"] == "completed"
    assert result["region"] == "Dortmund"


def test_classification_result_handler_rejects_invalid_label(
    result_handler,
):
    """An empty classifier label must be rejected."""

    prediction = {
        "label": "",
        "confidence": 0.92,
    }

    with pytest.raises(ValueError):
        result_handler.handle(prediction)


def test_classification_result_handler_rejects_invalid_confidence(
    result_handler,
):
    """Confidence must be between 0 and 1."""

    prediction = {
        "label": "glass jar",
        "confidence": 1.5,
    }

    with pytest.raises(ValueError):
        result_handler.handle(prediction)


def test_classification_result_handler_uses_dortmund_by_default(
    result_handler,
):
    """Dortmund should be the default region."""

    prediction = {
        "label": "glass jar",
        "confidence": 0.92,
    }

    result = result_handler.handle(prediction)

    assert result["region"] == "Dortmund"


# ------------------------------------------------------------------
# GuidanceService tests
# ------------------------------------------------------------------

def test_guidance_service_returns_guidance_for_label(
    guidance_service,
):
    """
    GuidanceService should retrieve disposal guidance using
    the classifier label.
    """

    guidance = guidance_service.get_guidance("glass jar")

    assert guidance is not None
    assert guidance["label"] == "glass jar"
    assert guidance["category"] == "recyclable"
    assert guidance["region"] == "Dortmund"
    assert guidance["bin_type"] == (
        "Altglascontainer (glass container)"
    )


def test_guidance_service_uses_dortmund_by_default(
    guidance_service,
):
    """The default region should be Dortmund."""

    guidance = guidance_service.get_guidance("glass jar")

    assert guidance["region"] == "Dortmund"


def test_guidance_service_returns_none_for_unknown_label(
    guidance_service,
):
    """
    An unknown label should return None instead of creating
    an invalid disposal rule.
    """

    guidance = guidance_service.get_guidance(
        "unknown waste item"
    )

    assert guidance is None


def test_guidance_service_saves_classification(
    guidance_service,
):
    """A classification result should be saved in the database."""

    classification_id = guidance_service.save_classification(
        label="glass jar",
        confidence=0.92,
    )

    assert classification_id is not None
    assert isinstance(classification_id, int)
    assert classification_id > 0


# ------------------------------------------------------------------
# GuidanceService integration test
# ------------------------------------------------------------------

def test_guidance_service_processes_classification(
    guidance_service,
):
    """
    The service should retrieve guidance and save the
    classification as one backend operation.
    """

    classification = {
        "label": "glass jar",
        "confidence": 0.92,
        "status": "completed",
        "region": "Dortmund",
    }

    result = guidance_service.process_classification(
        classification
    )

    assert result["guidance"] is not None
    assert result["guidance"]["label"] == "glass jar"
    assert result["guidance"]["category"] == "recyclable"

    assert result["classification_id"] is not None
    assert isinstance(result["classification_id"], int)


# ------------------------------------------------------------------
# ResponseComposer tests
# ------------------------------------------------------------------

def test_response_composer_creates_frontend_response(
    response_composer,
):
    """The composer should create the final frontend response."""

    classification = {
        "label": "glass jar",
        "confidence": 0.92,
        "status": "completed",
        "region": "Dortmund",
    }

    guidance = {
        "label": "glass jar",
        "category": "recyclable",
        "is_deposit": False,
        "region": "Dortmund",
        "bin_type": "Altglascontainer (glass container)",
        "instruction": "Remove the lid. Sort by colour.",
    }

    response = response_composer.compose(
        classification=classification,
        guidance=guidance,
        classification_id=1,
    )

    assert response["api_version"] == "v1"
    assert response["status"] == "completed"

    assert response["classification"]["label"] == "glass jar"
    assert response["classification"]["confidence"] == 0.92
    assert response["classification"]["region"] == "Dortmund"

    assert response["disposal"]["category"] == "recyclable"
    assert response["disposal"]["region"] == "Dortmund"

    assert response["classification_id"] == 1


# ------------------------------------------------------------------
# End-to-end test for your backend subsystem
# ------------------------------------------------------------------

def test_backend_subsystem_end_to_end(
    result_handler,
    guidance_service,
    response_composer,
):
    """
    Test the complete flow of your subsystem:

        Classifier
            ↓
        ClassificationResultHandler
            ↓
        GuidanceService
            ↓
        DatabaseManager
            ↓
        ResponseComposer
            ↓
        Final frontend response
    """

    # Simulated output from the ML classifier
    classifier_prediction = {
        "label": "Glass Jar",
        "confidence": 0.92,
    }

    # Step 1: Handle classifier result
    classification = result_handler.handle(
        classifier_prediction
    )

    # Step 2: Retrieve guidance + save classification
    processed = guidance_service.process_classification(
        classification
    )

    # Step 3: Compose final response
    response = response_composer.compose(
        classification=classification,
        guidance=processed["guidance"],
        classification_id=processed["classification_id"],
    )

    # Verify final result
    assert response["api_version"] == "v1"
    assert response["status"] == "completed"

    assert response["classification"]["label"] == "glass jar"
    assert response["classification"]["confidence"] == 0.92

    assert response["classification"]["region"] == "Dortmund"

    assert response["disposal"]["category"] == "recyclable"
    assert response["disposal"]["region"] == "Dortmund"

    assert response["classification_id"] > 0