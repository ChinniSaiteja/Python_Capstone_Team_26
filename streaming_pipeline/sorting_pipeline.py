from typing import Iterable

from .pipeline_stage import PipelineStage
from .recognition_event import RecognitionEvent


class SortingPipeline:
    """
    Composes multiple PipelineStage objects into a processing pipeline.

    The | operator is overloaded to allow intuitive pipeline composition.

    Example:
        pipeline = ConfidenceFilter() | MaterialTransformer()
    """

    def __init__(self, stages: Iterable[PipelineStage] | None = None):
        self.__stages: list[PipelineStage] = []

        if stages is not None:
            for stage in stages:
                self.add_stage(stage)

    def add_stage(self, stage: PipelineStage) -> "SortingPipeline":
        if not isinstance(stage, PipelineStage):
            raise TypeError("stage must inherit from PipelineStage")

        if not stage.initialized:
            stage.initialize()

        self.__stages.append(stage)
        return self

    def __or__(self, other):
        """
        Overload | to compose pipeline stages.

        Example:
            filter_stage | transformer_stage
        """

        if isinstance(other, PipelineStage):
            new_pipeline = SortingPipeline(self.__stages)
            new_pipeline.add_stage(other)
            return new_pipeline

        if isinstance(other, SortingPipeline):
            new_pipeline = SortingPipeline(self.__stages)

            for stage in other.stages:
                new_pipeline.add_stage(stage)

            return new_pipeline

        return NotImplemented

    def process(self, event: RecognitionEvent) -> RecognitionEvent | None:
        current = event

        for stage in self.__stages:
            if current is None:
                return None

            current = stage.process(current)

        return current

    def process_stream(
        self,
        events: Iterable[RecognitionEvent],
    ) -> list[RecognitionEvent]:
        results = []

        for event in events:
            result = self.process(event)

            if result is not None:
                results.append(result)

        return results

    @property
    def stages(self) -> tuple[PipelineStage, ...]:
        return tuple(self.__stages)

    def __len__(self) -> int:
        return len(self.__stages)

    def __repr__(self) -> str:
        names = " | ".join(stage.name for stage in self.__stages)
        return f"SortingPipeline({names})"