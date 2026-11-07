from streaming_pipeline import ConfidenceFilter, RecognitionEvent


def make_event(confidence):
    return RecognitionEvent(
        label="PET_BOTTLE",
        confidence=confidence,
        bounding_box=(10, 20, 100, 200),
        visual_tags=["plastic", "bottle"],
    )


def test_high_confidence_event_is_accepted():
    stage = ConfidenceFilter(threshold=0.5)
    stage.initialize()

    event = make_event(0.9)

    result = stage.process(event)

    assert result is event
    assert result.accepted is True


def test_low_confidence_event_is_rejected():
    stage = ConfidenceFilter(threshold=0.5)
    stage.initialize()

    event = make_event(0.3)

    result = stage.process(event)

    assert result is None
    assert event.accepted is False


def test_threshold_getter_setter():
    stage = ConfidenceFilter(0.5)

    assert stage.threshold == 0.5

    stage.threshold = 0.7

    assert stage.threshold == 0.7