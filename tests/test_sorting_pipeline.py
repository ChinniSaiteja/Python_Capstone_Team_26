from streaming_pipeline import (
    ConfidenceFilter,
    MaterialTransformer,
    RecognitionEvent,
    SortingPipeline,
)


def make_event(label="PET_BOTTLE", confidence=0.95):
    return RecognitionEvent(
        label=label,
        confidence=confidence,
        bounding_box=(10, 20, 100, 200),
        visual_tags=["plastic", "bottle"],
    )


def test_operator_overloading_composes_stages():
    confidence_filter = ConfidenceFilter(0.5)
    transformer = MaterialTransformer()

    pipeline = confidence_filter | transformer

    assert len(pipeline) == 2
    assert pipeline.stages[0] is confidence_filter
    assert pipeline.stages[1] is transformer


def test_pipeline_processes_event():
    pipeline = ConfidenceFilter(0.5) | MaterialTransformer()

    result = pipeline.process(make_event())

    assert result is not None
    assert result.material == "PET"
    assert result.routing_code == "ROUTE_PET"


def test_pipeline_rejects_low_confidence_event():
    pipeline = ConfidenceFilter(0.5) | MaterialTransformer()

    result = pipeline.process(make_event(confidence=0.2))

    assert result is None