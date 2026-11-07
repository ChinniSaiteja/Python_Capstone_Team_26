from streaming_pipeline import EventGenerator, RecognitionEvent


def make_events():
    return [
        RecognitionEvent(
            label="PET_BOTTLE",
            confidence=0.95,
            bounding_box=(1, 2, 3, 4),
        ),
        RecognitionEvent(
            label="ALUMINUM_CAN",
            confidence=0.90,
            bounding_box=(5, 6, 7, 8),
        ),
    ]


def test_event_generator_is_iterator():
    generator = EventGenerator(make_events())

    assert iter(generator) is generator


def test_event_generator_returns_events():
    generator = EventGenerator(make_events())

    first = next(generator)
    second = next(generator)

    assert first.label == "PET_BOTTLE"
    assert second.label == "ALUMINUM_CAN"


def test_event_generator_stops():
    generator = EventGenerator(make_events())

    list(generator)

    try:
        next(generator)
        assert False
    except StopIteration:
        pass