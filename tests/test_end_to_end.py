from streaming_pipeline import (
    ConfidenceFilter,
    EventGenerator,
    MaterialTransformer,
    RecognitionEvent,
    SortingPipeline,
)


def test_end_to_end_stream_processing():
    events = [
        RecognitionEvent(
            label="PET_BOTTLE",
            confidence=0.95,
            bounding_box=(10, 20, 100, 200),
            visual_tags=["plastic", "bottle"],
        ),
        RecognitionEvent(
            label="ALUMINUM_CAN",
            confidence=0.91,
            bounding_box=(30, 40, 80, 120),
            visual_tags=["metal", "can"],
        ),
        RecognitionEvent(
            label="HDPE_BOTTLE",
            confidence=0.35,
            bounding_box=(50, 60, 90, 150),
            visual_tags=["plastic", "bottle"],
        ),
    ]

    stream = EventGenerator(events)

    pipeline = ConfidenceFilter(0.5) | MaterialTransformer()

    results = []

    for event in stream:
        result = pipeline.process(event)

        if result is not None:
            results.append(result)

    assert len(results) == 2

    assert results[0].material == "PET"
    assert results[0].routing_code == "ROUTE_PET"

    assert results[1].material == "ALUMINUM"
    assert results[1].routing_code == "ROUTE_ALUMINUM"