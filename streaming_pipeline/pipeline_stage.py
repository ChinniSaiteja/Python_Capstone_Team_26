from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")
R = TypeVar("R")


class PipelineStage(ABC, Generic[T, R]):
    """
    Abstract base class for all stream-processing stages.
    """

    def __init__(self, name: str):
        self.__name = name
        self.__initialized = False

    def initialize(self):
        """Initialize the pipeline stage."""
        self.__initialized = True

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Stage name must be a non-empty string")
        self.__name = value.strip()

    @property
    def initialized(self) -> bool:
        return self.__initialized

    @abstractmethod
    def process(self, event: T) -> R:
        """
        Process one event.

        Every concrete pipeline stage must implement this method.
        """
        pass

    def __or__(self, other):
        """
        Compose this stage with another stage using the | operator.

        Example:
            ConfidenceFilter(0.5) | MaterialTransformer()
        """
        from .sorting_pipeline import SortingPipeline

        return SortingPipeline([self, other])