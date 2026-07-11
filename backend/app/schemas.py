from pydantic import BaseModel
from typing import List


class TopPrediction(BaseModel):
    class_name_es: str
    confidence: float


class PredictionResponse(BaseModel):
    """Schema for the /predict endpoint response."""

    class_name: str
    class_name_es: str
    plant: str
    confidence: float
    is_healthy: bool
    description: str
    severity: str
    treatment: str
    gradcam_image: str  # base64-encoded PNG with heatmap overlay (or original image fallback)
    top_predictions: List[TopPrediction]

