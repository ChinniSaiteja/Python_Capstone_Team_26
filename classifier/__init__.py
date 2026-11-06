"""Subsystem 3 - Computer Vision Classifier Model (Azam Rahmani, Team 26).

The backend only needs:

    from classifier import WasteClassifier
    result = WasteClassifier().classify(image_bytes_or_path)
"""

from classifier.category_mapper import CategoryMapper
from classifier.config import ClassifierConfig
from classifier.evaluator import ModelEvaluator
from classifier.model import ClassifierModel, ZeroShotClipModel
from classifier.preprocessor import ImagePreprocessor, InvalidImageError
from classifier.result import PredictionResult
from classifier.status import ClassifierStatus
from classifier.waste_classifier import WasteClassifier

__all__ = [
    "CategoryMapper",
    "ClassifierConfig",
    "ClassifierModel",
    "ClassifierStatus",
    "ImagePreprocessor",
    "InvalidImageError",
    "ModelEvaluator",
    "PredictionResult",
    "WasteClassifier",
    "ZeroShotClipModel",
]
