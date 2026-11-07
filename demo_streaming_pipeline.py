from streaming_pipeline import (
    ConfidenceFilter,
    EventGenerator,
    MaterialTransformer,
    RecognitionEvent,
)


def main():
    events = [
        RecognitionEvent(
            label="PET_BOTTLE",
            confidence=0.94,
            bounding_box=(120, 80, 240, 300),
            visual_tags=["plastic", "bottle"],
        ),
        RecognitionEvent(
            label="HDPE_BOTTLE",
            confidence=0.88,
            bounding_box=(100, 60, 210, 280),
            visual_tags=["plastic", "bottle"],
        ),
        RecognitionEvent(
            label="ALUMINUM_CAN",
            confidence=0.91,
            bounding_box=(50, 40, 130, 180),
            visual_tags=["metal", "can"],
        ),
        RecognitionEvent(
            label="PET_BOTTLE",
            confidence=0.32,
            bounding_box=(70, 50, 160, 220),
            visual_tags=["plastic", "bottle"],
        ),
    ]

    event_stream = EventGenerator(events)

    pipeline = ConfidenceFilter(0.50) | MaterialTransformer()

    print("=" * 60)
    print("AI-POWERED WASTE SORTING STREAMING PIPELINE")
    print("=" * 60)

    for event in event_stream:
        print(f"\nIncoming event:")
        print(f"  Label:       {event.label}")
        print(f"  Confidence:  {event.confidence:.2f}")

        result = pipeline.process(event)

        if result is None:
            print("  Result:      REJECTED - low confidence")
        else:
            print(f"  Material:    {result.material}")
            print(f"  Routing:     {result.routing_code}")
            print("  Result:      ACCEPTED")


if __name__ == "__main__":
    main()