from dataclasses import dataclass, field
from typing import Any


@dataclass
class RecognitionEvent:
    """Represents one real-time waste recognition event."""

    label: str
    confidence: float
    bounding_box: tuple[int, int, int, int] | list[int]
    visual_tags: list[str] = field(default_factory=list)

    material: str | None = None
    routing_code: str | None = None
    accepted: bool = True

    def __post_init__(self):
        if not self.label:
            raise ValueError("label cannot be empty")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

        if len(self.bounding_box) != 4:
            raise ValueError("bounding_box must contain four values")

    def to_dict(self) -> dict[str, Any]:
        """Convert the event into a dictionary."""

        return {
            "label": self.label,
            "confidence": self.confidence,
            "bounding_box": list(self.bounding_box),
            "visual_tags": list(self.visual_tags),
            "material": self.material,
            "routing_code": self.routing_code,
            "accepted": self.accepted,
        }

    def __repr__(self) -> str:
        return (
            f"RecognitionEvent("
            f"label='{self.label}', "
            f"confidence={self.confidence:.2f}, "
            f"material='{self.material}', "
            f"routing_code='{self.routing_code}', "
            f"accepted={self.accepted})"
        )