from dataclasses import dataclass, field


@dataclass
class ClassifierConfig:
    """All tunable settings of the classifier in one place."""

    model_name: str = "openai/clip-vit-base-patch32"
    confidence_threshold: float = 0.5
    image_size: int = 224
    max_file_size_mb: float = 10.0
    allowed_formats: tuple = ("JPEG", "PNG", "WEBP")
    prompt_template: str = "a photo of {}"
    device: str = field(default="cpu")

    def __post_init__(self):
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1")
        if self.image_size <= 0:
            raise ValueError("image_size must be positive")
