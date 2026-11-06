import io

import pytest
from PIL import Image

from classifier import ClassifierConfig, ClassifierModel, WasteClassifier


class FakeModel(ClassifierModel):
    """Stands in for CLIP so tests run in milliseconds without downloads."""

    def __init__(self, label="glass jar", confidence=0.92, error=None):
        super().__init__(ClassifierConfig(), labels=[label])
        self.label = label
        self.confidence = confidence
        self.error = error
        self.calls = 0

    def predict(self, image):
        self.calls += 1
        if self.error:
            raise self.error
        return self.label, self.confidence


def make_image_bytes(fmt="JPEG", size=(64, 48), mode="RGB"):
    buffer = io.BytesIO()
    Image.new(mode, size, color=(120, 200, 80) if mode == "RGB" else 0).save(buffer, format=fmt)
    return buffer.getvalue()


@pytest.fixture
def jpeg_bytes():
    return make_image_bytes("JPEG")


@pytest.fixture
def jpeg_file(tmp_path, jpeg_bytes):
    path = tmp_path / "item.jpg"
    path.write_bytes(jpeg_bytes)
    return path


@pytest.fixture
def make_classifier():
    def _make(**model_kwargs):
        return WasteClassifier(model=FakeModel(**model_kwargs))

    return _make
