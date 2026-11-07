from streaming_pipeline import MaterialTransformer, RecognitionEvent


def test_pet_bottle_is_transformed_to_pet():
    transformer = MaterialTransformer()
    transformer.initialize()

    event = RecognitionEvent(
        label="PET_BOTTLE",
        confidence=0.95,
        bounding_box=(1, 2, 3, 4),
        visual_tags=["plastic"],
    )

    result = transformer.process(event)

    assert result.material == "PET"
    assert result.routing_code == "ROUTE_PET"


def test_aluminum_can_is_transformed():
    transformer = MaterialTransformer()
    transformer.initialize()

    event = RecognitionEvent(
        label="ALUMINUM_CAN",
        confidence=0.90,
        bounding_box=(1, 2, 3, 4),
    )

    result = transformer.process(event)

    assert result.material == "ALUMINUM"
    assert result.routing_code == "ROUTE_ALUMINUM"


def test_unknown_material():
    transformer = MaterialTransformer()
    transformer.initialize()

    event = RecognitionEvent(
        label="UNKNOWN_OBJECT",
        confidence=0.90,
        bounding_box=(1, 2, 3, 4),
    )

    result = transformer.process(event)

    assert result.material == "UNKNOWN"
    assert result.routing_code == "ROUTE_UNKNOWN"