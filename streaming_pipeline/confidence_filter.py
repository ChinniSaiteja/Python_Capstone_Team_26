from .pipeline_stage import PipelineStage
from .recognition_event import RecognitionEvent


class ConfidenceFilter(PipelineStage[RecognitionEvent, RecognitionEvent | None]):
    """
    Filters recognition events based on confidence.

    Events below the configured threshold are rejected.
    """

    def __init__(self, threshold: float = 0.50):
        super().__init__("Confidence Filter")

        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")

        self.__threshold = threshold

    def initialize(self) -> None:
        super().initialize()

    @property
    def threshold(self) -> float:
        return self.__threshold

    @threshold.setter
    def threshold(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError("threshold must be between 0 and 1")

        self.__threshold = value

    def process(self, data: RecognitionEvent) -> RecognitionEvent | None:
        if not isinstance(data, RecognitionEvent):
            raise TypeError("data must be a RecognitionEvent")

        if data.confidence < self.__threshold:
            data.accepted = False
            return None

        data.accepted = True
        return data