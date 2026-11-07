from .pipeline_stage import PipelineStage
from .recognition_event import RecognitionEvent


class MaterialTransformer(PipelineStage[RecognitionEvent, RecognitionEvent]):
    """
    Transforms object recognition labels into material categories
    and conveyor routing codes.
    """

    DEFAULT_MATERIAL_MAPPING = {
        "PET_BOTTLE": "PET",
        "PET": "PET",
        "HDPE_BOTTLE": "HDPE",
        "HDPE": "HDPE",
        "ALUMINUM_CAN": "ALUMINUM",
        "ALUMINIUM_CAN": "ALUMINUM",
        "ALUMINUM": "ALUMINUM",
        "GLASS_BOTTLE": "GLASS",
        "GLASS": "GLASS",
        "PAPER": "PAPER",
        "CARDBOARD": "CARDBOARD",
    }

    DEFAULT_ROUTING_MAPPING = {
        "PET": "ROUTE_PET",
        "HDPE": "ROUTE_HDPE",
        "ALUMINUM": "ROUTE_ALUMINUM",
        "GLASS": "ROUTE_GLASS",
        "PAPER": "ROUTE_PAPER",
        "CARDBOARD": "ROUTE_CARDBOARD",
    }

    def __init__(
        self,
        material_mapping: dict[str, str] | None = None,
        routing_mapping: dict[str, str] | None = None,
    ):
        super().__init__("Material Transformer")

        self.__material_mapping = (
            material_mapping.copy()
            if material_mapping is not None
            else self.DEFAULT_MATERIAL_MAPPING.copy()
        )

        self.__routing_mapping = (
            routing_mapping.copy()
            if routing_mapping is not None
            else self.DEFAULT_ROUTING_MAPPING.copy()
        )

    def initialize(self) -> None:
        super().initialize()

    @property
    def material_mapping(self) -> dict[str, str]:
        return self.__material_mapping.copy()

    @material_mapping.setter
    def material_mapping(self, value: dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("material_mapping must be a dictionary")

        self.__material_mapping = value.copy()

    @property
    def routing_mapping(self) -> dict[str, str]:
        return self.__routing_mapping.copy()

    @routing_mapping.setter
    def routing_mapping(self, value: dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("routing_mapping must be a dictionary")

        self.__routing_mapping = value.copy()

    def process(self, data: RecognitionEvent) -> RecognitionEvent:
        if not isinstance(data, RecognitionEvent):
            raise TypeError("data must be a RecognitionEvent")

        normalized_label = data.label.upper().strip()

        material = self.__material_mapping.get(
            normalized_label,
            "UNKNOWN",
        )

        routing_code = self.__routing_mapping.get(
            material,
            "ROUTE_UNKNOWN",
        )

        data.material = material
        data.routing_code = routing_code

        return data